import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QFileDialog, QProgressBar, QFrame, QMessageBox
)

from interface.telas.tela_base import TelaBase
from interface.componentes.trabalhador import TarefaSegundoPlano
from conversores.converter_pdf import ConversorPDF
from conversores.converter_word import ConversorWord
from conversores.converter_imagem import ConversorImagem
from conversores.converter_dados import ConversorDados

class TelaConversor(TelaBase):
    def __init__(self):
        super().__init__("Conversor Inteligente Multiformato")
        self.caminho_arquivo = ""
        self.tarefa_atual: TarefaSegundoPlano | None = None
        
        self.configurar_interface()

    def configurar_interface(self):
        cartao = QFrame()
        cartao.setObjectName("Cartao")
        layout_cartao = QVBoxLayout(cartao)
        layout_cartao.setSpacing(14)
        layout_cartao.setContentsMargins(18, 18, 18, 18)

        rotulo_informacao = QLabel("Selecione um arquivo de documento, imagem ou planilha para converter com alta fidelidade.")
        rotulo_informacao.setWordWrap(True)
        rotulo_informacao.setStyleSheet("color: #555047; font-size: 13px;")
        layout_cartao.addWidget(rotulo_informacao)

        linha_arquivo = QHBoxLayout()
        self.botao_selecionar = QPushButton("Selecionar Arquivo")
        self.botao_selecionar.clicked.connect(self.selecionar_arquivo)
        self.rotulo_caminho = QLabel("Nenhum arquivo carregado")
        self.rotulo_caminho.setStyleSheet("color: #7A7469; font-style: italic;")
        linha_arquivo.addWidget(self.botao_selecionar)
        linha_arquivo.addWidget(self.rotulo_caminho, 1)
        layout_cartao.addLayout(linha_arquivo)

        linha_acoes = QHBoxLayout()
        rotulo_destino = QLabel("Formato de Destino:")
        rotulo_destino.setStyleSheet("font-weight: bold;")
        
        self.combo_destino = QComboBox()
        self.combo_destino.setEnabled(False)
        self.combo_destino.setMinimumWidth(220)

        self.botao_converter = QPushButton("Converter Arquivo")
        self.botao_converter.setProperty("primario", "true")
        self.botao_converter.setEnabled(False)
        self.botao_converter.clicked.connect(self.iniciar_conversao)

        linha_acoes.addWidget(rotulo_destino)
        linha_acoes.addWidget(self.combo_destino)
        linha_acoes.addStretch()
        linha_acoes.addWidget(self.botao_converter)
        layout_cartao.addLayout(linha_acoes)

        self.barra_progresso = QProgressBar()
        self.barra_progresso.setTextVisible(True)
        self.barra_progresso.setValue(0)
        self.barra_progresso.hide()
        layout_cartao.addWidget(self.barra_progresso)

        self.rotulo_status = QLabel("Aguardando arquivo.")
        self.rotulo_status.setWordWrap(True)
        self.rotulo_status.setStyleSheet("color: #4A463F; font-size: 13px; font-weight: 500;")
        layout_cartao.addWidget(self.rotulo_status)

        self.layout_conteudo.addWidget(cartao)
        self.layout_conteudo.addStretch()

    def selecionar_arquivo(self):
        filtros = (
            "Todos os Suportados (*.pdf *.docx *.png *.jpg *.jpeg *.csv *.xlsx *.json);;"
            "Documentos PDF (*.pdf);;"
            "Documentos Word (*.docx);;"
            "Imagens (*.png *.jpg *.jpeg);;"
            "Tabelas e Dados (*.csv *.xlsx *.json)"
        )
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo para Conversão", "", filtros)
        if not arquivo:
            return

        self.caminho_arquivo = arquivo
        nome_arquivo = os.path.basename(arquivo)
        self.rotulo_caminho.setText(f"{nome_arquivo} ({os.path.dirname(arquivo)})")
        self.rotulo_caminho.setStyleSheet("color: #2C2926; font-weight: bold;")
        
        extensao = os.path.splitext(arquivo)[1].lower()
        self.combo_destino.clear()

        if extensao == ".pdf":
            self.combo_destino.addItems([
                "Microsoft Word (.docx)",
                "Markdown (.md)",
                "Texto Puro (.txt)",
                "Extrair Páginas em Imagens (.png)"
            ])
        elif extensao == ".docx":
            self.combo_destino.addItems([
                "Documento PDF (.pdf)",
                "Markdown (.md)",
                "Texto Puro (.txt)",
                "Página Web HTML (.html)"
            ])
        elif extensao in [".png", ".jpg", ".jpeg"]:
            self.combo_destino.addItems([
                "Documento PDF (.pdf)",
                "Imagem PNG (.png)",
                "Imagem JPEG (.jpg)"
            ])
        elif extensao == ".csv":
            self.combo_destino.addItems([
                "Planilha Excel (.xlsx)"
            ])
        elif extensao in [".xlsx", ".xls"]:
            self.combo_destino.addItems([
                "Tabela CSV (.csv)"
            ])
        elif extensao == ".json":
            self.combo_destino.addItems([
                "Planilha Excel (.xlsx)",
                "Tabela CSV (.csv)"
            ])
        else:
            self.rotulo_status.setText(f"Formato {extensao} não suportado para conversão direta.")
            self.combo_destino.setEnabled(False)
            self.botao_converter.setEnabled(False)
            return

        self.combo_destino.setEnabled(True)
        self.botao_converter.setEnabled(True)
        self.rotulo_status.setText("Selecione o formato de destino e clique em 'Converter Arquivo'.")

    def iniciar_conversao(self):
        if not self.caminho_arquivo:
            return

        destino = self.combo_destino.currentText()
        extensao_original = os.path.splitext(self.caminho_arquivo)[1].lower()

        if ".docx" in destino:
            extensao_saida = ".docx"
            filtro = "Word (*.docx)"
        elif ".md" in destino:
            extensao_saida = ".md"
            filtro = "Markdown (*.md)"
        elif ".txt" in destino:
            extensao_saida = ".txt"
            filtro = "Texto (*.txt)"
        elif ".pdf" in destino:
            extensao_saida = ".pdf"
            filtro = "PDF (*.pdf)"
        elif ".html" in destino:
            extensao_saida = ".html"
            filtro = "HTML (*.html)"
        elif ".png" in destino and "Extrair" in destino:
            pasta_destino = QFileDialog.getExistingDirectory(self, "Selecionar Pasta para Salvar Imagens")
            if not pasta_destino:
                return
            self.executar_tarefa(ConversorPDF.para_imagens, self.caminho_arquivo, pasta_destino, "png", True)
            return
        elif ".png" in destino:
            extensao_saida = ".png"
            filtro = "Imagem PNG (*.png)"
        elif ".jpg" in destino:
            extensao_saida = ".jpg"
            filtro = "Imagem JPEG (*.jpg)"
        elif ".xlsx" in destino:
            extensao_saida = ".xlsx"
            filtro = "Excel (*.xlsx)"
        elif ".csv" in destino:
            extensao_saida = ".csv"
            filtro = "CSV (*.csv)"
        else:
            return

        sugestao = os.path.splitext(self.caminho_arquivo)[0] + "_convertido" + extensao_saida
        arquivo_saida, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo Convertido", sugestao, filtro)
        if not arquivo_saida:
            return

        if os.path.abspath(arquivo_saida) == os.path.abspath(self.caminho_arquivo):
            QMessageBox.warning(
                self, "Aviso", 
                "O arquivo de destino não pode ser idêntico ao arquivo de origem na conversão de formato."
            )
            return

        funcao = None
        argumentos = []

        if extensao_original == ".pdf":
            if extensao_saida == ".docx":
                funcao = ConversorPDF.para_word
                argumentos = [self.caminho_arquivo, arquivo_saida]
            elif extensao_saida == ".md":
                funcao = ConversorPDF.para_markdown
                argumentos = [self.caminho_arquivo, arquivo_saida]
            elif extensao_saida == ".txt":
                funcao = ConversorPDF.para_texto
                argumentos = [self.caminho_arquivo, arquivo_saida]
        elif extensao_original == ".docx":
            if extensao_saida == ".pdf":
                funcao = ConversorWord.para_pdf
                argumentos = [self.caminho_arquivo, arquivo_saida]
            elif extensao_saida == ".md":
                funcao = ConversorWord.para_markdown
                argumentos = [self.caminho_arquivo, arquivo_saida]
            elif extensao_saida == ".txt":
                funcao = ConversorWord.para_texto
                argumentos = [self.caminho_arquivo, arquivo_saida]
            elif extensao_saida == ".html":
                funcao = ConversorWord.para_html
                argumentos = [self.caminho_arquivo, arquivo_saida]
        elif extensao_original in [".png", ".jpg", ".jpeg"]:
            if extensao_saida == ".pdf":
                funcao = ConversorImagem.para_pdf
                argumentos = [[self.caminho_arquivo], arquivo_saida]
            elif extensao_saida in [".png", ".jpg"]:
                funcao = ConversorImagem.converter_formato
                argumentos = [self.caminho_arquivo, arquivo_saida, extensao_saida.replace(".", "")]
        elif extensao_original == ".csv" and extensao_saida == ".xlsx":
            funcao = ConversorDados.csv_para_excel
            argumentos = [self.caminho_arquivo, arquivo_saida]
        elif extensao_original in [".xlsx", ".xls"] and extensao_saida == ".csv":
            funcao = ConversorDados.excel_para_csv
            argumentos = [self.caminho_arquivo, arquivo_saida]
        elif extensao_original == ".json":
            if extensao_saida == ".xlsx":
                funcao = ConversorDados.json_para_excel
                argumentos = [self.caminho_arquivo, arquivo_saida]
            elif extensao_saida == ".csv":
                funcao = ConversorDados.json_para_csv
                argumentos = [self.caminho_arquivo, arquivo_saida]

        if funcao:
            self.executar_tarefa(funcao, *argumentos)

    def executar_tarefa(self, funcao, *argumentos):
        self.botao_selecionar.setEnabled(False)
        self.botao_converter.setEnabled(False)
        self.combo_destino.setEnabled(False)
        self.barra_progresso.show()
        self.barra_progresso.setRange(0, 0)
        self.rotulo_status.setText("Convertendo arquivo em segundo plano...")

        self.tarefa_atual = TarefaSegundoPlano(funcao, *argumentos)
        self.tarefa_atual.sucesso.connect(self.ao_sucesso)
        self.tarefa_atual.erro.connect(self.ao_erro)
        self.tarefa_atual.start()

    def ao_sucesso(self, resultado):
        self.barra_progresso.hide()
        self.botao_selecionar.setEnabled(True)
        self.botao_converter.setEnabled(True)
        self.combo_destino.setEnabled(True)

        if isinstance(resultado, list):
            mensagem = f"Conversão concluída com sucesso! {len(resultado)} arquivos gerados."
        else:
            mensagem = f"Conversão concluída com sucesso!\nSalvo em: {resultado}"
            
        self.rotulo_status.setText(mensagem)
        QMessageBox.information(self, "Sucesso", mensagem)

    def ao_erro(self, mensagem_erro: str):
        self.barra_progresso.hide()
        self.botao_selecionar.setEnabled(True)
        self.botao_converter.setEnabled(True)
        self.combo_destino.setEnabled(True)
        self.rotulo_status.setText(f"Erro na conversão: {mensagem_erro.splitlines()[0]}")
        QMessageBox.critical(self, "Erro na Conversão", f"Ocorreu um erro ao processar o arquivo:\n\n{mensagem_erro}")

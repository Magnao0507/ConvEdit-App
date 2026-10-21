import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFileDialog, QScrollArea, QTabWidget, QProgressBar, 
    QFrame, QMessageBox, QSplitter
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from interface.telas.tela_base import TelaBase
from interface.componentes.trabalhador import TarefaSegundoPlano
from editor.comparador_pdf import ComparadorVisual
from editor.operacoes_pdf import OperacoesPDF

class TelaComparador(TelaBase):
    def __init__(self):
        super().__init__("Comparador Visual de PDFs (Diff Tool)")
        self.caminho_pdf1 = ""
        self.caminho_pdf2 = ""
        self.pagina_atual = 0
        self.total_paginas = 0
        self.tarefa_atual: TarefaSegundoPlano | None = None

        self.configurar_interface()

    def configurar_interface(self):
        layout = self.layout_conteudo
        layout.setSpacing(10)

        cartao_arquivos = QFrame()
        cartao_arquivos.setObjectName("Cartao")
        layout_arquivos = QVBoxLayout(cartao_arquivos)
        layout_arquivos.setSpacing(8)
        layout_arquivos.setContentsMargins(12, 10, 12, 10)

        linha1 = QHBoxLayout()
        self.botao_selecionar_pdf1 = QPushButton("Selecionar PDF 1 (Original)")
        self.botao_selecionar_pdf1.clicked.connect(self.selecionar_pdf1)
        self.rotulo_pdf1 = QLabel("Nenhum arquivo selecionado")
        self.rotulo_pdf1.setStyleSheet("color: #7A7469; font-style: italic;")
        linha1.addWidget(self.botao_selecionar_pdf1)
        linha1.addWidget(self.rotulo_pdf1, 1)
        layout_arquivos.addLayout(linha1)

        linha2 = QHBoxLayout()
        self.botao_selecionar_pdf2 = QPushButton("Selecionar PDF 2 (Modificado)")
        self.botao_selecionar_pdf2.clicked.connect(self.selecionar_pdf2)
        self.rotulo_pdf2 = QLabel("Nenhum arquivo selecionado")
        self.rotulo_pdf2.setStyleSheet("color: #7A7469; font-style: italic;")
        linha2.addWidget(self.botao_selecionar_pdf2)
        linha2.addWidget(self.rotulo_pdf2, 1)
        layout_arquivos.addLayout(linha2)

        layout.addWidget(cartao_arquivos)

        linha_controles = QHBoxLayout()
        
        self.botao_anterior = QPushButton("Página Anterior")
        self.botao_anterior.clicked.connect(self.pagina_anterior)
        self.botao_anterior.setEnabled(False)

        self.rotulo_pagina = QLabel("Página: 0 / 0")
        self.rotulo_pagina.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.botao_proxima = QPushButton("Próxima Página")
        self.botao_proxima.clicked.connect(self.pagina_proxima)
        self.botao_proxima.setEnabled(False)

        self.botao_comparar_atual = QPushButton("Atualizar Comparação")
        self.botao_comparar_atual.setProperty("primario", "true")
        self.botao_comparar_atual.clicked.connect(self.comparar_pagina_atual)
        self.botao_comparar_atual.setEnabled(False)

        self.botao_exportar_tudo = QPushButton("Exportar Todas as Diferenças...")
        self.botao_exportar_tudo.clicked.connect(self.exportar_todas_diferencas)
        self.botao_exportar_tudo.setEnabled(False)

        linha_controles.addWidget(self.botao_anterior)
        linha_controles.addWidget(self.rotulo_pagina)
        linha_controles.addWidget(self.botao_proxima)
        linha_controles.addSpacing(20)
        linha_controles.addWidget(self.botao_comparar_atual)
        linha_controles.addStretch()
        linha_controles.addWidget(self.botao_exportar_tudo)
        layout.addLayout(linha_controles)

        self.abas_visualizacao = QTabWidget()
        
        scroll_diff = QScrollArea()
        scroll_diff.setWidgetResizable(True)
        self.rotulo_imagem_diff = QLabel("Selecione ambos os PDFs para visualizar as diferenças.")
        self.rotulo_imagem_diff.setAlignment(Qt.AlignCenter)
        self.rotulo_imagem_diff.setStyleSheet("color: #7A7469; font-size: 14px; padding: 20px;")
        scroll_diff.setWidget(self.rotulo_imagem_diff)
        self.abas_visualizacao.addTab(scroll_diff, "Diferenças Destacadas")

        painel_lado_a_lado = QWidget()
        layout_lado = QHBoxLayout(painel_lado_a_lado)
        layout_lado.setContentsMargins(0, 0, 0, 0)

        divisor = QSplitter(Qt.Horizontal)
        
        box1 = QVBoxLayout()
        box1.addWidget(QLabel("<b>Original (PDF 1)</b>", alignment=Qt.AlignCenter))
        scroll1 = QScrollArea()
        scroll1.setWidgetResizable(True)
        self.rotulo_imagem1 = QLabel("Aguardando PDF 1", alignment=Qt.AlignCenter)
        scroll1.setWidget(self.rotulo_imagem1)
        widget1 = QWidget()
        widget1.setLayout(box1)
        box1.addWidget(scroll1)
        divisor.addWidget(widget1)

        box2 = QVBoxLayout()
        box2.addWidget(QLabel("<b>Modificado (PDF 2)</b>", alignment=Qt.AlignCenter))
        scroll2 = QScrollArea()
        scroll2.setWidgetResizable(True)
        self.rotulo_imagem2 = QLabel("Aguardando PDF 2", alignment=Qt.AlignCenter)
        scroll2.setWidget(self.rotulo_imagem2)
        widget2 = QWidget()
        widget2.setLayout(box2)
        box2.addWidget(scroll2)
        divisor.addWidget(widget2)

        layout_lado.addWidget(divisor)
        self.abas_visualizacao.addTab(painel_lado_a_lado, "Visualização Lado a Lado")

        layout.addWidget(self.abas_visualizacao, 1)

        self.barra_progresso = QProgressBar()
        self.barra_progresso.setTextVisible(True)
        self.barra_progresso.hide()
        layout.addWidget(self.barra_progresso)

        self.rotulo_status = QLabel("Pronto para comparar versões de documentos.")
        self.rotulo_status.setStyleSheet("color: #4A463F; font-size: 13px;")
        layout.addWidget(self.rotulo_status)

    def selecionar_pdf1(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF 1 (Original)", "", "Documentos PDF (*.pdf)")
        if caminho:
            self.caminho_pdf1 = caminho
            self.rotulo_pdf1.setText(os.path.basename(caminho))
            self.rotulo_pdf1.setStyleSheet("color: #2C2926; font-weight: bold;")
            self.verificar_ambos_arquivos()

    def selecionar_pdf2(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF 2 (Modificado)", "", "Documentos PDF (*.pdf)")
        if caminho:
            self.caminho_pdf2 = caminho
            self.rotulo_pdf2.setText(os.path.basename(caminho))
            self.rotulo_pdf2.setStyleSheet("color: #2C2926; font-weight: bold;")
            self.verificar_ambos_arquivos()

    def verificar_ambos_arquivos(self):
        if self.caminho_pdf1 and self.caminho_pdf2:
            try:
                informacoes1 = OperacoesPDF.obter_informacoes(self.caminho_pdf1)
                informacoes2 = OperacoesPDF.obter_informacoes(self.caminho_pdf2)
                self.total_paginas = max(informacoes1["total_paginas"], informacoes2["total_paginas"])
                self.pagina_atual = 0
                self.atualizar_controles_navegacao()
                self.botao_comparar_atual.setEnabled(True)
                self.botao_exportar_tudo.setEnabled(True)
                self.rotulo_status.setText(
                    f"Arquivos carregados. PDF 1: {informacoes1['total_paginas']} págs | PDF 2: {informacoes2['total_paginas']} págs."
                )
                self.comparar_pagina_atual()
            except Exception as excecao:
                QMessageBox.critical(self, "Erro", f"Erro ao ler arquivos: {str(excecao)}")

    def atualizar_controles_navegacao(self):
        self.rotulo_pagina.setText(f"Página: {self.pagina_atual + 1} / {self.total_paginas}")
        self.botao_anterior.setEnabled(self.pagina_atual > 0)
        self.botao_proxima.setEnabled(self.pagina_atual < self.total_paginas - 1)

    def pagina_anterior(self):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.atualizar_controles_navegacao()
            self.comparar_pagina_atual()

    def pagina_proxima(self):
        if self.pagina_atual < self.total_paginas - 1:
            self.pagina_atual += 1
            self.atualizar_controles_navegacao()
            self.comparar_pagina_atual()

    def comparar_pagina_atual(self):
        if not self.caminho_pdf1 or not self.caminho_pdf2:
            return

        self.rotulo_imagem_diff.setText("Renderizando e calculando diferenças da página...")
        self.rotulo_imagem1.setText("Carregando...")
        self.rotulo_imagem2.setText("Carregando...")

        def tarefa():
            bytes_diferenca, alterado = ComparadorVisual.gerar_imagem_diff(self.caminho_pdf1, self.caminho_pdf2, self.pagina_atual)
            bytes_pagina1 = ComparadorVisual.renderizar_pagina(self.caminho_pdf1, self.pagina_atual)
            bytes_pagina2 = ComparadorVisual.renderizar_pagina(self.caminho_pdf2, self.pagina_atual)
            return bytes_diferenca, alterado, bytes_pagina1, bytes_pagina2

        self.tarefa_atual = TarefaSegundoPlano(tarefa)
        self.tarefa_atual.sucesso.connect(self.ao_sucesso_renderizacao)
        self.tarefa_atual.erro.connect(self.ao_erro_renderizacao)
        self.tarefa_atual.start()

    def ao_sucesso_renderizacao(self, dados):
        bytes_diferenca, alterado, bytes_pagina1, bytes_pagina2 = dados

        if bytes_diferenca:
            pixmap_diff = QPixmap()
            pixmap_diff.loadFromData(bytes_diferenca)
            self.rotulo_imagem_diff.setPixmap(pixmap_diff)
            self.rotulo_imagem_diff.setText("")
        else:
            self.rotulo_imagem_diff.setPixmap(QPixmap())
            self.rotulo_imagem_diff.setText("Página inexistente.")

        if bytes_pagina1:
            pixmap1 = QPixmap()
            pixmap1.loadFromData(bytes_pagina1)
            self.rotulo_imagem1.setPixmap(pixmap1)
            self.rotulo_imagem1.setText("")
        else:
            self.rotulo_imagem1.setPixmap(QPixmap())
            self.rotulo_imagem1.setText("Esta página não existe no PDF 1.")

        if bytes_pagina2:
            pixmap2 = QPixmap()
            pixmap2.loadFromData(bytes_pagina2)
            self.rotulo_imagem2.setPixmap(pixmap2)
            self.rotulo_imagem2.setText("")
        else:
            self.rotulo_imagem2.setPixmap(QPixmap())
            self.rotulo_imagem2.setText("Esta página não existe no PDF 2.")

        if alterado:
            self.rotulo_status.setText(f"Divergências detectadas na página {self.pagina_atual + 1} (destacadas em vermelho).")
            self.rotulo_status.setStyleSheet("color: #9C413E; font-weight: bold; font-size: 13px;")
        else:
            self.rotulo_status.setText(f"Páginas idênticas na página {self.pagina_atual + 1}.")
            self.rotulo_status.setStyleSheet("color: #2F6932; font-weight: bold; font-size: 13px;")

    def ao_erro_renderizacao(self, mensagem_erro: str):
        self.rotulo_status.setText(f"Erro ao comparar: {mensagem_erro}")
        self.rotulo_imagem_diff.setText("Erro ao renderizar imagem de diferença.")

    def exportar_todas_diferencas(self):
        if not self.caminho_pdf1 or not self.caminho_pdf2:
            return

        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta para Salvar Imagens de Diferenças")
        if not pasta:
            return

        self.botao_anterior.setEnabled(False)
        self.botao_proxima.setEnabled(False)
        self.botao_comparar_atual.setEnabled(False)
        self.botao_exportar_tudo.setEnabled(False)
        self.barra_progresso.show()
        self.barra_progresso.setRange(0, 100)
        self.barra_progresso.setValue(5)
        self.rotulo_status.setText("Comparando todas as páginas e exportando relatórios visuais...")

        self.tarefa_atual = TarefaSegundoPlano(ComparadorVisual.comparar_documento_completo, self.caminho_pdf1, self.caminho_pdf2, pasta)
        self.tarefa_atual.progresso.connect(self.ao_progresso_exportacao)
        self.tarefa_atual.sucesso.connect(self.ao_sucesso_exportacao)
        self.tarefa_atual.erro.connect(self.ao_erro_exportacao)
        self.tarefa_atual.start()

    def ao_progresso_exportacao(self, porcentagem: int, mensagem: str):
        self.barra_progresso.setValue(porcentagem)
        self.rotulo_status.setText(mensagem)

    def ao_sucesso_exportacao(self, resultado):
        self.barra_progresso.hide()
        self.atualizar_controles_navegacao()
        self.botao_comparar_atual.setEnabled(True)
        self.botao_exportar_tudo.setEnabled(True)
        mensagem = f"Exportação concluída com sucesso. {len(resultado)} imagens de comparação foram salvas na pasta selecionada."
        self.rotulo_status.setText(mensagem)
        QMessageBox.information(self, "Exportação Concluída", mensagem)

    def ao_erro_exportacao(self, mensagem_erro: str):
        self.barra_progresso.hide()
        self.atualizar_controles_navegacao()
        self.botao_comparar_atual.setEnabled(True)
        self.botao_exportar_tudo.setEnabled(True)
        self.rotulo_status.setText("Erro na exportação de diferenças.")
        QMessageBox.critical(self, "Erro", f"Falha ao exportar:\n\n{mensagem_erro}")

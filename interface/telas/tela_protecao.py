import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QCheckBox, QLineEdit, QFileDialog, QTabWidget, 
    QProgressBar, QFrame, QMessageBox
)

from interface.telas.tela_base import TelaBase
from interface.componentes.trabalhador import TarefaSegundoPlano
from editor.redacao_pdf import ManipuladorRedacao
from editor.operacoes_pdf import OperacoesPDF

class TelaProtecao(TelaBase):
    def __init__(self):
        super().__init__("Higienização e Proteção LGPD")
        self.caminho_arquivo = ""
        self.caminho_marca = ""
        self.tarefa_atual: TarefaSegundoPlano | None = None
        
        self.configurar_interface()

    def configurar_interface(self):
        self.abas = QTabWidget()
        
        self.aba_lgpd = self.criar_aba_lgpd()
        self.aba_marca_dagua = self.criar_aba_marca_dagua()
        
        self.abas.addTab(self.aba_lgpd, "Higienização LGPD e Dados Sensíveis")
        self.abas.addTab(self.aba_marca_dagua, "Marcas d'Água Corporativas")
        
        self.layout_conteudo.addWidget(self.abas)

        self.barra_progresso = QProgressBar()
        self.barra_progresso.setTextVisible(True)
        self.barra_progresso.hide()
        self.layout_conteudo.addWidget(self.barra_progresso)

        self.rotulo_status = QLabel("Selecione um arquivo PDF para higienizar ou proteger.")
        self.rotulo_status.setStyleSheet("color: #4A463F; font-size: 13px; font-weight: 500;")
        self.layout_conteudo.addWidget(self.rotulo_status)

    def criar_aba_lgpd(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(14)

        caixa_alerta = QFrame()
        caixa_alerta.setObjectName("Cartao")
        layout_alerta = QVBoxLayout(caixa_alerta)
        rotulo_aviso = QLabel(
            "A redação do Convedit é definitiva: os dados selecionados são fisicamente removidos do PDF, "
            "impedindo seleção de texto, leitores de tela ou engenharia reversa, atendendo às normas de sigilo e LGPD."
        )
        rotulo_aviso.setWordWrap(True)
        rotulo_aviso.setStyleSheet("color: #3E5F5A; font-size: 13px;")
        layout_alerta.addWidget(rotulo_aviso)
        layout.addWidget(caixa_alerta)

        linha_selecao = QHBoxLayout()
        self.botao_selecionar_lgpd = QPushButton("Selecionar PDF")
        self.botao_selecionar_lgpd.clicked.connect(self.selecionar_pdf_lgpd)
        self.rotulo_pdf_lgpd = QLabel("Nenhum PDF selecionado")
        self.rotulo_pdf_lgpd.setStyleSheet("color: #7A7469; font-style: italic;")
        linha_selecao.addWidget(self.botao_selecionar_lgpd)
        linha_selecao.addWidget(self.rotulo_pdf_lgpd, 1)
        layout.addLayout(linha_selecao)

        cartao_opcoes = QFrame()
        cartao_opcoes.setObjectName("Cartao")
        layout_opcoes = QVBoxLayout(cartao_opcoes)
        layout_opcoes.setSpacing(10)

        rotulo_padroes = QLabel("Padrões para Detecção Automática:")
        rotulo_padroes.setStyleSheet("font-weight: bold;")
        layout_opcoes.addWidget(rotulo_padroes)

        self.check_cpf = QCheckBox("Tarjar números de CPF (com ou sem pontuação)")
        self.check_cpf.setChecked(True)
        self.check_email = QCheckBox("Tarjar endereços de e-mail")
        self.check_email.setChecked(True)
        self.check_telefone = QCheckBox("Tarjar telefones e celulares")
        self.check_telefone.setChecked(True)

        layout_opcoes.addWidget(self.check_cpf)
        layout_opcoes.addWidget(self.check_email)
        layout_opcoes.addWidget(self.check_telefone)
        layout.addWidget(cartao_opcoes)

        rotulo_termos = QLabel("Palavras-chave, nomes ou valores adicionais a censurar (separados por vírgula):")
        rotulo_termos.setStyleSheet("font-weight: bold;")
        layout.addWidget(rotulo_termos)

        self.campo_termos = QLineEdit()
        self.campo_termos.setPlaceholderText("Ex: João da Silva, Conta Corrente, 123.456-7, R$ 1.000.000,00")
        layout.addWidget(self.campo_termos)

        linha_tarja = QHBoxLayout()
        rotulo_texto_tarja = QLabel("Texto gravado na tarja preta (opcional):")
        self.campo_texto_tarja = QLineEdit()
        self.campo_texto_tarja.setText("[DADO PROTEGIDO]")
        self.campo_texto_tarja.setMaximumWidth(200)
        linha_tarja.addWidget(rotulo_texto_tarja)
        linha_tarja.addWidget(self.campo_texto_tarja)
        linha_tarja.addStretch()
        layout.addLayout(linha_tarja)

        self.botao_executar_redacao = QPushButton("Aplicar Redação Definitiva e Higienizar")
        self.botao_executar_redacao.setProperty("primario", "true")
        self.botao_executar_redacao.setEnabled(False)
        self.botao_executar_redacao.clicked.connect(self.executar_redacao_lgpd)
        layout.addWidget(self.botao_executar_redacao)
        layout.addStretch()

        return widget

    def selecionar_pdf_lgpd(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF", "", "Documentos PDF (*.pdf)")
        if caminho:
            self.caminho_arquivo = caminho
            try:
                informacoes = OperacoesPDF.obter_informacoes(caminho)
                self.rotulo_pdf_lgpd.setText(f"{informacoes['nome_arquivo']} ({informacoes['total_paginas']} páginas)")
                self.rotulo_pdf_lgpd.setStyleSheet("color: #2C2926; font-weight: bold;")
            except Exception:
                self.rotulo_pdf_lgpd.setText(os.path.basename(caminho))
            self.botao_executar_redacao.setEnabled(True)

    def executar_redacao_lgpd(self):
        if not self.caminho_arquivo:
            return

        termos = [termo.strip() for termo in self.campo_termos.text().split(",") if termo.strip()]
        censurar_cpf = self.check_cpf.isChecked()
        censurar_email = self.check_email.isChecked()
        censurar_telefone = self.check_telefone.isChecked()
        texto_tarja = self.campo_texto_tarja.text().strip()

        if not termos and not censurar_cpf and not censurar_email and not censurar_telefone:
            QMessageBox.warning(self, "Aviso", "Selecione ao menos um padrão de dado sensível ou informe termos para censurar.")
            return

        sugestao = os.path.splitext(self.caminho_arquivo)[0] + "_higienizado.pdf"
        saida, _ = QFileDialog.getSaveFileName(self, "Salvar PDF Higienizado", sugestao, "Documentos PDF (*.pdf)")
        if not saida:
            return

        self.iniciar_tarefa(
            ManipuladorRedacao.higienizar_documento,
            self.caminho_arquivo, saida, termos,
            censurar_cpf, censurar_email, censurar_telefone, texto_tarja
        )

    def criar_aba_marca_dagua(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(14)

        linha_selecao = QHBoxLayout()
        self.botao_selecionar_marca = QPushButton("Selecionar PDF")
        self.botao_selecionar_marca.clicked.connect(self.selecionar_pdf_marca)
        self.rotulo_pdf_marca = QLabel("Nenhum PDF selecionado")
        self.rotulo_pdf_marca.setStyleSheet("color: #7A7469; font-style: italic;")
        linha_selecao.addWidget(self.botao_selecionar_marca)
        linha_selecao.addWidget(self.rotulo_pdf_marca, 1)
        layout.addLayout(linha_selecao)

        cartao = QFrame()
        cartao.setObjectName("Cartao")
        layout_cartao = QVBoxLayout(cartao)

        rotulo_texto = QLabel("Texto da Marca d'Água:")
        rotulo_texto.setStyleSheet("font-weight: bold;")
        layout_cartao.addWidget(rotulo_texto)

        self.campo_marca = QLineEdit()
        self.campo_marca.setText("CONFIDENCIAL")
        layout_cartao.addWidget(self.campo_marca)

        layout.addWidget(cartao)

        self.botao_aplicar_marca = QPushButton("Inserir Marca d'Água em Todas as Páginas")
        self.botao_aplicar_marca.setProperty("primario", "true")
        self.botao_aplicar_marca.setEnabled(False)
        self.botao_aplicar_marca.clicked.connect(self.executar_marca_dagua)
        layout.addWidget(self.botao_aplicar_marca)
        layout.addStretch()

        return widget

    def selecionar_pdf_marca(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF", "", "Documentos PDF (*.pdf)")
        if caminho:
            self.caminho_marca = caminho
            self.rotulo_pdf_marca.setText(os.path.basename(caminho))
            self.rotulo_pdf_marca.setStyleSheet("color: #2C2926; font-weight: bold;")
            self.botao_aplicar_marca.setEnabled(True)

    def executar_marca_dagua(self):
        if not self.caminho_marca:
            return

        texto = self.campo_marca.text().strip()
        if not texto:
            QMessageBox.warning(self, "Aviso", "Digite o texto da marca d'água.")
            return

        sugestao = os.path.splitext(self.caminho_marca)[0] + "_com_marca.pdf"
        saida, _ = QFileDialog.getSaveFileName(self, "Salvar PDF com Marca", sugestao, "Documentos PDF (*.pdf)")
        if not saida:
            return

        self.iniciar_tarefa(ManipuladorRedacao.adicionar_marca_dagua, self.caminho_marca, saida, texto)

    def iniciar_tarefa(self, funcao, *argumentos):
        self.abas.setEnabled(False)
        self.barra_progresso.show()
        self.barra_progresso.setRange(0, 100)
        self.barra_progresso.setValue(10)
        self.rotulo_status.setText("Processando higienização do documento...")

        self.tarefa_atual = TarefaSegundoPlano(funcao, *argumentos)
        self.tarefa_atual.progresso.connect(self.ao_progresso)
        self.tarefa_atual.sucesso.connect(self.ao_sucesso)
        self.tarefa_atual.erro.connect(self.ao_erro)
        self.tarefa_atual.start()

    def ao_progresso(self, porcentagem: int, mensagem: str):
        self.barra_progresso.setValue(porcentagem)
        self.rotulo_status.setText(mensagem)

    def ao_sucesso(self, resultado):
        self.barra_progresso.hide()
        self.abas.setEnabled(True)

        if isinstance(resultado, dict) and 'total_redacoes' in resultado:
            total = resultado['total_redacoes']
            paginas = resultado['paginas_afetadas']
            mensagem = (
                f"Higienização finalizada com êxito.\n\n"
                f"Total de dados censurados: {total}\n"
                f"Páginas higienizadas: {', '.join(map(str, paginas)) if paginas else 'Nenhuma'}\n"
                f"Arquivo limpo salvo em:\n{resultado['caminho_saida']}"
            )
            self.rotulo_status.setText(f"Higienização concluída: {total} redações aplicadas com segurança.")
            QMessageBox.information(self, "Higienização Concluída", mensagem)
        else:
            mensagem = f"Operação concluída com sucesso.\nSalvo em: {resultado}"
            self.rotulo_status.setText(mensagem)
            QMessageBox.information(self, "Sucesso", mensagem)

    def ao_erro(self, mensagem_erro: str):
        self.barra_progresso.hide()
        self.abas.setEnabled(True)
        self.rotulo_status.setText("Erro ao higienizar documento.")
        QMessageBox.critical(self, "Erro na Proteção", f"Ocorreu um erro durante o processo:\n\n{mensagem_erro}")

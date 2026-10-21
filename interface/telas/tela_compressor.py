import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFileDialog, QComboBox, QProgressBar, QFrame, QMessageBox
)

from interface.telas.tela_base import TelaBase
from interface.componentes.trabalhador import TarefaSegundoPlano
from editor.compressao_pdf import CompressorPDF
from editor.operacoes_pdf import OperacoesPDF

class TelaCompressor(TelaBase):
    def __init__(self):
        super().__init__("Compressão Otimizada (Redução de Tamanho)")
        self.caminho_arquivo = ""
        self.tarefa_atual: TarefaSegundoPlano | None = None
        
        self.configurar_interface()

    def configurar_interface(self):
        layout = self.layout_conteudo
        layout.setSpacing(14)

        cartao = QFrame()
        cartao.setObjectName("Cartao")
        layout_cartao = QVBoxLayout(cartao)
        layout_cartao.setSpacing(14)
        layout_cartao.setContentsMargins(18, 18, 18, 18)

        info = QLabel(
            "Otimize e reduza o peso dos seus arquivos PDF para envio por e-mail ou armazenamento em nuvem, "
            "removendo objetos órfãos, dados duplicados e compactando fluxos internos."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #555047; font-size: 13px;")
        layout_cartao.addWidget(info)

        linha_arquivo = QHBoxLayout()
        self.botao_selecionar = QPushButton("Selecionar PDF")
        self.botao_selecionar.clicked.connect(self.selecionar_arquivo)
        self.rotulo_arquivo = QLabel("Nenhum PDF selecionado")
        self.rotulo_arquivo.setStyleSheet("color: #7A7469; font-style: italic;")
        linha_arquivo.addWidget(self.botao_selecionar)
        linha_arquivo.addWidget(self.rotulo_arquivo, 1)
        layout_cartao.addLayout(linha_arquivo)

        linha_nivel = QHBoxLayout()
        rotulo_nivel = QLabel("Nível de Otimização:")
        rotulo_nivel.setStyleSheet("font-weight: bold;")
        
        self.combo_nivel = QComboBox()
        self.combo_nivel.addItem("Equilibrado (Recomendado - remove órfãos e comprime fluxos)", "equilibrado")
        self.combo_nivel.addItem("Leve (Rápido, apenas compactação de fluxos)", "leve")
        self.combo_nivel.addItem("Máximo (Limpeza profunda e compactação total de fontes/fluxos)", "maximo")

        self.botao_comprimir = QPushButton("Comprimir PDF")
        self.botao_comprimir.setProperty("primario", "true")
        self.botao_comprimir.setEnabled(False)
        self.botao_comprimir.clicked.connect(self.comprimir_arquivo)

        linha_nivel.addWidget(rotulo_nivel)
        linha_nivel.addWidget(self.combo_nivel, 1)
        linha_nivel.addSpacing(15)
        linha_nivel.addWidget(self.botao_comprimir)
        layout_cartao.addLayout(linha_nivel)

        layout.addWidget(cartao)

        self.cartao_resultado = QFrame()
        self.cartao_resultado.setObjectName("Cartao")
        layout_resultado = QVBoxLayout(self.cartao_resultado)
        layout_resultado.setSpacing(8)
        layout_resultado.setContentsMargins(18, 15, 18, 15)

        rotulo_resultado_titulo = QLabel("Estatísticas da Otimização:")
        rotulo_resultado_titulo.setStyleSheet("font-weight: bold; font-size: 14px; color: #3E5F5A;")
        layout_resultado.addWidget(rotulo_resultado_titulo)

        self.rotulo_estatisticas = QLabel("As métricas de redução aparecerão aqui após a compressão.")
        self.rotulo_estatisticas.setStyleSheet("color: #555047; font-size: 13px; line-height: 1.5;")
        layout_resultado.addWidget(self.rotulo_estatisticas)

        layout.addWidget(self.cartao_resultado)

        self.barra_progresso = QProgressBar()
        self.barra_progresso.setTextVisible(True)
        self.barra_progresso.hide()
        layout.addWidget(self.barra_progresso)

        self.rotulo_status = QLabel("Aguardando arquivo.")
        self.rotulo_status.setStyleSheet("color: #4A463F; font-size: 13px; font-weight: 500;")
        layout.addWidget(self.rotulo_status)

        layout.addStretch()

    def selecionar_arquivo(self):
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF para Compressão", "", "Documentos PDF (*.pdf)")
        if arquivo:
            self.caminho_arquivo = arquivo
            try:
                informacoes = OperacoesPDF.obter_informacoes(arquivo)
                self.rotulo_arquivo.setText(f"{informacoes['nome_arquivo']} ({informacoes['total_paginas']} págs | {informacoes['tamanho_formatado']})")
                self.rotulo_arquivo.setStyleSheet("color: #2C2926; font-weight: bold;")
            except Exception:
                self.rotulo_arquivo.setText(os.path.basename(arquivo))
                
            self.botao_comprimir.setEnabled(True)
            self.rotulo_status.setText("Arquivo pronto para compressão. Escolha o nível e clique em 'Comprimir PDF'.")

    def comprimir_arquivo(self):
        if not self.caminho_arquivo:
            return

        nivel = self.combo_nivel.currentData()
        sugestao = os.path.splitext(self.caminho_arquivo)[0] + "_otimizado.pdf"
        arquivo_saida, _ = QFileDialog.getSaveFileName(self, "Salvar PDF Comprimido", sugestao, "Documentos PDF (*.pdf)")
        if not arquivo_saida:
            return

        self.botao_selecionar.setEnabled(False)
        self.botao_comprimir.setEnabled(False)
        self.combo_nivel.setEnabled(False)
        self.barra_progresso.show()
        self.barra_progresso.setRange(0, 100)
        self.barra_progresso.setValue(10)
        self.rotulo_status.setText("Comprimindo e limpando documento...")

        self.tarefa_atual = TarefaSegundoPlano(CompressorPDF.comprimir_pdf, self.caminho_arquivo, arquivo_saida, nivel)
        self.tarefa_atual.progresso.connect(self.ao_progresso)
        self.tarefa_atual.sucesso.connect(self.ao_sucesso)
        self.tarefa_atual.erro.connect(self.ao_erro)
        self.tarefa_atual.start()

    def ao_progresso(self, porcentagem: int, mensagem: str):
        self.barra_progresso.setValue(porcentagem)
        self.rotulo_status.setText(mensagem)

    def ao_sucesso(self, estatisticas: dict):
        self.barra_progresso.hide()
        self.botao_selecionar.setEnabled(True)
        self.botao_comprimir.setEnabled(True)
        self.combo_nivel.setEnabled(True)

        tamanho_original_mb = estatisticas['tamanho_original'] / (1024 * 1024)
        novo_tamanho_mb = estatisticas['novo_tamanho'] / (1024 * 1024)
        bytes_salvos_kb = estatisticas['bytes_salvos'] / 1024
        
        texto_resultado = (
            f"<b>Tamanho Original:</b> {tamanho_original_mb:.2f} MB ({estatisticas['tamanho_original']:,} bytes)<br>"
            f"<b>Novo Tamanho:</b> {novo_tamanho_mb:.2f} MB ({estatisticas['novo_tamanho']:,} bytes)<br>"
            f"<b>Espaço Economizado:</b> {bytes_salvos_kb:.1f} KB (<b>{estatisticas['proporcao']}% de redução</b>)<br>"
            f"<b>Salvo em:</b> {estatisticas['caminho_saida']}"
        )
        self.rotulo_estatisticas.setText(texto_resultado)
        self.rotulo_status.setText(f"Compressão concluída com sucesso. Redução de {estatisticas['proporcao']}%.")
        self.rotulo_status.setStyleSheet("color: #2F6932; font-weight: bold;")

        QMessageBox.information(
            self, "Compressão Concluída", 
            f"O PDF foi otimizado com sucesso.\n\n"
            f"Tamanho Original: {tamanho_original_mb:.2f} MB\n"
            f"Novo Tamanho: {novo_tamanho_mb:.2f} MB\n"
            f"Redução Obtida: {estatisticas['proporcao']}%\n\n"
            f"Salvo em: {estatisticas['caminho_saida']}"
        )

    def ao_erro(self, mensagem_erro: str):
        self.barra_progresso.hide()
        self.botao_selecionar.setEnabled(True)
        self.botao_comprimir.setEnabled(True)
        self.combo_nivel.setEnabled(True)
        self.rotulo_status.setText("Erro ao comprimir PDF.")
        self.rotulo_status.setStyleSheet("color: #9C413E; font-weight: bold;")
        QMessageBox.critical(self, "Erro na Compressão", f"Ocorreu uma falha ao comprimir o arquivo:\n\n{mensagem_erro}")

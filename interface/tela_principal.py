from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
    QPushButton, QStackedWidget, QLabel
)
from PySide6.QtCore import Qt

from interface.telas.tela_conversor import TelaConversor
from interface.telas.tela_editor import TelaEditor
from interface.telas.tela_protecao import TelaProtecao
from interface.telas.tela_comparador import TelaComparador
from interface.telas.tela_compressor import TelaCompressor

class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convedit - Editor Profissional de Documentos")
        self.setMinimumSize(1024, 768)

        self.iniciar_interface()

    def iniciar_interface(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_principal = QHBoxLayout(widget_central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        self.painel_lateral = QFrame()
        self.painel_lateral.setObjectName("PainelLateral")
        self.painel_lateral.setFixedWidth(250)
        layout_lateral = QVBoxLayout(self.painel_lateral)
        layout_lateral.setContentsMargins(10, 20, 10, 20)
        layout_lateral.setSpacing(10)

        rotulo_titulo = QLabel("Convedit")
        rotulo_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C2926;")
        rotulo_titulo.setAlignment(Qt.AlignCenter)
        layout_lateral.addWidget(rotulo_titulo)
        layout_lateral.addSpacing(20)

        self.botoes_navegacao: list[QPushButton] = []
        modulos = [
            ("Conversor Inteligente", 0),
            ("Editor Profissional", 1),
            ("Higienização e LGPD", 2),
            ("Comparador Visual", 3),
            ("Compressão Otimizada", 4)
        ]

        self.painel_telas = QStackedWidget()

        self.telas = {
            0: TelaConversor(),
            1: TelaEditor(),
            2: TelaProtecao(),
            3: TelaComparador(),
            4: TelaCompressor()
        }

        for nome, indice in modulos:
            botao = QPushButton(nome)
            botao.setProperty("class", "BotaoLateral")
            botao.setCheckable(True)
            botao.clicked.connect(lambda checado, indice_modulo=indice: self.trocar_modulo(indice_modulo))
            self.botoes_navegacao.append(botao)
            layout_lateral.addWidget(botao)

            self.painel_telas.addWidget(self.telas[indice])

        layout_lateral.addStretch()

        rotulo_assinatura = QLabel("Desenvolvido por Arthur Magno")
        rotulo_assinatura.setStyleSheet("font-size: 11px; color: #827B70; padding-top: 10px;")
        rotulo_assinatura.setAlignment(Qt.AlignCenter)
        layout_lateral.addWidget(rotulo_assinatura)

        layout_principal.addWidget(self.painel_lateral)
        layout_principal.addWidget(self.painel_telas)

        if self.botoes_navegacao:
            self.botoes_navegacao[0].setChecked(True)
            self.trocar_modulo(0)

    def trocar_modulo(self, indice: int):
        for posicao, botao in enumerate(self.botoes_navegacao):
            botao.setChecked(posicao == indice)
        self.painel_telas.setCurrentIndex(indice)

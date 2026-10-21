from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class TelaBase(QWidget):
    def __init__(self, titulo):
        super().__init__()
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(10)
        
        # Título
        self.rotulo_titulo = QLabel(titulo)
        self.rotulo_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C2926;")
        self.layout_principal.addWidget(self.rotulo_titulo)
        
        # Área Principal
        self.area_conteudo = QWidget()
        self.area_conteudo.setObjectName("AreaDocumento")
        self.layout_conteudo = QVBoxLayout(self.area_conteudo)
        
        self.layout_principal.addWidget(self.area_conteudo)

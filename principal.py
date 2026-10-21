import sys
from PySide6.QtWidgets import QApplication
from interface.tela_principal import TelaPrincipal
from interface.tema_cores import obter_folha_estilos

def principal():
    """Ponto de entrada principal da aplicação Convedit."""
    aplicacao = QApplication(sys.argv)
    aplicacao.setStyleSheet(obter_folha_estilos())
    
    janela_principal = TelaPrincipal()
    janela_principal.show()
    
    sys.exit(aplicacao.exec())

if __name__ == "__main__":
    principal()

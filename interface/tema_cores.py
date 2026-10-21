def obter_folha_estilos() -> str:
    """Retorna a folha de estilos padronizada (QSS) da aplicação."""
    return """
    QWidget {
        background-color: #F4F1EA;
        color: #2C2926;
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 14px;
    }

    QFrame#PainelLateral, QFrame#Cartao {
        background-color: #EAE5DC;
        border: 1px solid #D5CFC3;
        border-radius: 8px;
    }

    QGraphicsView, QScrollArea, QFrame#AreaDocumento {
        background-color: #FAF8F5;
        border: 1px solid #D5CFC3;
        border-radius: 6px;
    }

    QFrame.LinhaVertical, QFrame.LinhaHorizontal {
        background-color: #D5CFC3;
    }

    QPushButton {
        background-color: #EAE5DC;
        border: 1px solid #D5CFC3;
        border-radius: 5px;
        padding: 7px 14px;
        color: #2C2926;
        font-weight: 500;
    }

    QPushButton:hover {
        background-color: #DFDAD1;
        border-color: #B8B0A2;
    }

    QPushButton:pressed {
        background-color: #827B70;
        color: #F4F1EA;
        border: 1px solid #827B70;
    }

    QPushButton:disabled {
        background-color: #EAE5DC;
        color: #9C968B;
        border-color: #E0DDD5;
    }

    QPushButton[primario="true"] {
        background-color: #3E5F5A;
        color: #FFFFFF;
        border: 1px solid #324D49;
        font-weight: bold;
    }

    QPushButton[primario="true"]:hover {
        background-color: #4C726C;
        border-color: #3E5F5A;
    }

    QPushButton[primario="true"]:pressed {
        background-color: #2C4340;
    }

    QPushButton[primario="true"]:disabled {
        background-color: #8CA29E;
        color: #E2E8E7;
        border-color: #8CA29E;
    }

    QPushButton[perigo="true"] {
        background-color: #A34843;
        color: #FFFFFF;
        border: 1px solid #893B37;
    }

    QPushButton[perigo="true"]:hover {
        background-color: #B8524C;
    }

    QPushButton[perigo="true"]:pressed {
        background-color: #7A3532;
    }

    QPushButton.BotaoLateral {
        background-color: transparent;
        border: none;
        text-align: left;
        padding: 10px 15px;
        border-radius: 6px;
        font-weight: bold;
        color: #3E3B37;
    }

    QPushButton.BotaoLateral:hover {
        background-color: #DFDAD1;
    }

    QPushButton.BotaoLateral:checked {
        background-color: #827B70;
        color: #F4F1EA;
    }

    QLineEdit, QComboBox, QSpinBox {
        background-color: #FAF8F5;
        border: 1px solid #D5CFC3;
        border-radius: 4px;
        padding: 6px 8px;
        color: #2C2926;
        selection-background-color: #827B70;
    }

    QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
        border: 1px solid #3E5F5A;
    }

    QComboBox::drop-down {
        border: none;
        padding-right: 8px;
    }

    QTextEdit, QPlainTextEdit {
        background-color: #FAF8F5;
        border: 1px solid #D5CFC3;
        border-radius: 4px;
        padding: 8px;
        color: #2C2926;
        selection-background-color: #827B70;
    }

    QListWidget {
        background-color: #FAF8F5;
        border: 1px solid #D5CFC3;
        border-radius: 5px;
        padding: 4px;
    }

    QListWidget::item {
        padding: 7px 10px;
        border-radius: 4px;
        margin-bottom: 2px;
    }

    QListWidget::item:hover {
        background-color: #EFECE5;
    }

    QListWidget::item:selected {
        background-color: #827B70;
        color: #FAF8F5;
    }

    QTabWidget::pane {
        border: 1px solid #D5CFC3;
        border-radius: 6px;
        background-color: #FAF8F5;
        top: -1px;
    }

    QTabBar::tab {
        background: #EAE5DC;
        border: 1px solid #D5CFC3;
        padding: 8px 18px;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        margin-right: 2px;
        font-weight: 500;
    }

    QTabBar::tab:hover {
        background: #DFDAD1;
    }

    QTabBar::tab:selected {
        background: #FAF8F5;
        border-bottom-color: #FAF8F5;
        font-weight: bold;
        color: #2C2926;
    }

    QGroupBox {
        font-weight: bold;
        border: 1px solid #D5CFC3;
        border-radius: 6px;
        margin-top: 12px;
        padding-top: 14px;
        background-color: #FAF8F5;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        padding: 0 4px;
        background-color: #FAF8F5;
        color: #2C2926;
    }

    QCheckBox, QRadioButton {
        spacing: 8px;
    }

    QCheckBox::indicator, QRadioButton::indicator {
        width: 16px;
        height: 16px;
    }

    QProgressBar {
        border: 1px solid #D5CFC3;
        border-radius: 4px;
        text-align: center;
        background-color: #EAE5DC;
        height: 16px;
        font-size: 12px;
        font-weight: bold;
    }

    QProgressBar::chunk {
        background-color: #3E5F5A;
        border-radius: 3px;
    }

    QScrollBar:vertical {
        border: none;
        background: #F4F1EA;
        width: 10px;
        margin: 0px;
    }

    QScrollBar::handle:vertical {
        background: #D5CFC3;
        min-height: 25px;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical:hover {
        background: #827B70;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    """

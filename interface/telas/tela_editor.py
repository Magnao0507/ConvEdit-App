import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QListWidget, QFileDialog, QTabWidget, QRadioButton, 
    QLineEdit, QSpinBox, QProgressBar, QFrame, QMessageBox, 
    QButtonGroup, QListWidgetItem
)
from PySide6.QtCore import Qt

from interface.telas.tela_base import TelaBase
from interface.componentes.trabalhador import TarefaSegundoPlano
from editor.operacoes_pdf import OperacoesPDF

class TelaEditor(TelaBase):
    def __init__(self):
        super().__init__("Editor Profissional de PDF")
        self.tarefa_atual: TarefaSegundoPlano | None = None
        self.caminho_pdf_dividir = ""
        self.total_paginas_dividir = 1
        self.caminho_pdf_organizar = ""

        self.configurar_interface()

    def configurar_interface(self):
        self.abas = QTabWidget()
        
        self.aba_mesclar = self.criar_aba_mesclar()
        self.aba_dividir = self.criar_aba_dividir()
        self.aba_organizar = self.criar_aba_organizar()
        
        self.abas.addTab(self.aba_mesclar, "Mesclar Documentos")
        self.abas.addTab(self.aba_dividir, "Dividir e Extrair")
        self.abas.addTab(self.aba_organizar, "Girar e Organizar")
        
        self.layout_conteudo.addWidget(self.abas)

        self.barra_progresso = QProgressBar()
        self.barra_progresso.setTextVisible(True)
        self.barra_progresso.hide()
        self.layout_conteudo.addWidget(self.barra_progresso)

        self.rotulo_status = QLabel("Selecione uma ferramenta acima para gerenciar seus arquivos PDF.")
        self.rotulo_status.setStyleSheet("color: #4A463F; font-size: 13px; font-weight: 500;")
        self.layout_conteudo.addWidget(self.rotulo_status)

    def criar_aba_mesclar(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        info = QLabel("Adicione os arquivos PDF na ordem que deseja combiná-los. Você pode alterar a ordem dos itens da lista.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #555047; font-size: 13px;")
        layout.addWidget(info)

        self.lista_mesclar = QListWidget()
        layout.addWidget(self.lista_mesclar)

        linha_controles = QHBoxLayout()
        self.botao_adicionar_pdf = QPushButton("Adicionar PDFs...")
        self.botao_adicionar_pdf.clicked.connect(self.adicionar_pdfs_mesclar)

        self.botao_subir_pdf = QPushButton("Subir")
        self.botao_subir_pdf.clicked.connect(self.subir_item_mesclar)

        self.botao_descer_pdf = QPushButton("Descer")
        self.botao_descer_pdf.clicked.connect(self.descer_item_mesclar)

        self.botao_remover_pdf = QPushButton("Remover")
        self.botao_remover_pdf.setProperty("perigo", "true")
        self.botao_remover_pdf.clicked.connect(self.remover_item_mesclar)

        self.botao_limpar_pdf = QPushButton("Limpar Todos")
        self.botao_limpar_pdf.clicked.connect(self.lista_mesclar.clear)

        linha_controles.addWidget(self.botao_adicionar_pdf)
        linha_controles.addWidget(self.botao_subir_pdf)
        linha_controles.addWidget(self.botao_descer_pdf)
        linha_controles.addWidget(self.botao_remover_pdf)
        linha_controles.addStretch()
        linha_controles.addWidget(self.botao_limpar_pdf)
        layout.addLayout(linha_controles)

        self.botao_executar_mesclar = QPushButton("Mesclar em um Único PDF")
        self.botao_executar_mesclar.setProperty("primario", "true")
        self.botao_executar_mesclar.clicked.connect(self.executar_mesclagem)
        layout.addWidget(self.botao_executar_mesclar)

        return widget

    def adicionar_pdfs_mesclar(self):
        arquivos, _ = QFileDialog.getOpenFileNames(self, "Selecionar PDFs para Mesclar", "", "Documentos PDF (*.pdf)")
        for caminho in arquivos:
            try:
                informacoes = OperacoesPDF.obter_informacoes(caminho)
                texto_item = f"{informacoes['nome_arquivo']}  ({informacoes['total_paginas']} págs | {informacoes['tamanho_formatado']})"
            except Exception:
                texto_item = os.path.basename(caminho)
                
            item = QListWidgetItem(texto_item)
            item.setData(Qt.UserRole, caminho)
            self.lista_mesclar.addItem(item)

    def subir_item_mesclar(self):
        indice = self.lista_mesclar.currentRow()
        if indice > 0:
            item = self.lista_mesclar.takeItem(indice)
            self.lista_mesclar.insertItem(indice - 1, item)
            self.lista_mesclar.setCurrentRow(indice - 1)

    def descer_item_mesclar(self):
        indice = self.lista_mesclar.currentRow()
        if 0 <= indice < self.lista_mesclar.count() - 1:
            item = self.lista_mesclar.takeItem(indice)
            self.lista_mesclar.insertItem(indice + 1, item)
            self.lista_mesclar.setCurrentRow(indice + 1)

    def remover_item_mesclar(self):
        indice = self.lista_mesclar.currentRow()
        if indice >= 0:
            self.lista_mesclar.takeItem(indice)

    def executar_mesclagem(self):
        total = self.lista_mesclar.count()
        if total < 2:
            QMessageBox.warning(self, "Aviso", "Adicione pelo menos 2 arquivos PDF para mesclar.")
            return

        caminhos = [self.lista_mesclar.item(i).data(Qt.UserRole) for i in range(total)]
        
        saida, _ = QFileDialog.getSaveFileName(self, "Salvar PDF Consolidado", "documento_mesclado.pdf", "PDF (*.pdf)")
        if not saida:
            return

        self.iniciar_tarefa(OperacoesPDF.mesclar, caminhos, saida)

    def criar_aba_dividir(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(14)

        linha_arquivo = QHBoxLayout()
        self.botao_selecionar_dividir = QPushButton("Selecionar PDF")
        self.botao_selecionar_dividir.clicked.connect(self.selecionar_pdf_dividir)
        self.rotulo_pdf_dividir = QLabel("Nenhum PDF selecionado")
        self.rotulo_pdf_dividir.setStyleSheet("color: #7A7469; font-style: italic;")
        linha_arquivo.addWidget(self.botao_selecionar_dividir)
        linha_arquivo.addWidget(self.rotulo_pdf_dividir, 1)
        layout.addLayout(linha_arquivo)

        caixa_opcoes = QFrame()
        caixa_opcoes.setObjectName("Cartao")
        layout_opcoes = QVBoxLayout(caixa_opcoes)
        
        rotulo_modo = QLabel("Modo de Divisão:")
        rotulo_modo.setStyleSheet("font-weight: bold;")
        layout_opcoes.addWidget(rotulo_modo)

        self.grupo_modo = QButtonGroup(self)
        self.radio_dividir_todas = QRadioButton("Dividir todas as páginas em arquivos individuais")
        self.radio_dividir_todas.setChecked(True)
        self.radio_intervalo = QRadioButton("Extrair intervalo específico de páginas")

        self.grupo_modo.addButton(self.radio_dividir_todas)
        self.grupo_modo.addButton(self.radio_intervalo)

        layout_opcoes.addWidget(self.radio_dividir_todas)
        layout_opcoes.addWidget(self.radio_intervalo)

        linha_intervalo = QHBoxLayout()
        rotulo_exemplo = QLabel("Intervalo (ex: 1-3, 5, 8-10):")
        self.campo_intervalo = QLineEdit()
        self.campo_intervalo.setPlaceholderText("Ex: 1-3, 5, 7")
        self.campo_intervalo.setEnabled(False)
        self.radio_intervalo.toggled.connect(self.campo_intervalo.setEnabled)

        linha_intervalo.addWidget(rotulo_exemplo)
        linha_intervalo.addWidget(self.campo_intervalo)
        layout_opcoes.addLayout(linha_intervalo)

        layout.addWidget(caixa_opcoes)

        self.botao_executar_divisao = QPushButton("Executar Divisão ou Extração")
        self.botao_executar_divisao.setProperty("primario", "true")
        self.botao_executar_divisao.setEnabled(False)
        self.botao_executar_divisao.clicked.connect(self.executar_divisao)
        layout.addWidget(self.botao_executar_divisao)
        layout.addStretch()

        return widget

    def selecionar_pdf_dividir(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF para Dividir", "", "Documentos PDF (*.pdf)")
        if caminho:
            self.caminho_pdf_dividir = caminho
            try:
                informacoes = OperacoesPDF.obter_informacoes(caminho)
                self.rotulo_pdf_dividir.setText(f"{informacoes['nome_arquivo']} ({informacoes['total_paginas']} páginas, {informacoes['tamanho_formatado']})")
                self.rotulo_pdf_dividir.setStyleSheet("color: #2C2926; font-weight: bold;")
                self.total_paginas_dividir = informacoes['total_paginas']
            except Exception:
                self.rotulo_pdf_dividir.setText(os.path.basename(caminho))
                self.total_paginas_dividir = 1
                
            self.botao_executar_divisao.setEnabled(True)

    def executar_divisao(self):
        if not self.caminho_pdf_dividir:
            return

        if self.radio_dividir_todas.isChecked():
            pasta = QFileDialog.getExistingDirectory(self, "Selecione a Pasta para Salvar as Páginas")
            if pasta:
                self.iniciar_tarefa(OperacoesPDF.dividir, self.caminho_pdf_dividir, pasta)
        else:
            texto = self.campo_intervalo.text().strip()
            if not texto:
                QMessageBox.warning(self, "Aviso", "Informe os números ou intervalos de páginas a extrair (ex: 1-3, 5).")
                return

            indices = self.interpretar_intervalo(texto, self.total_paginas_dividir)
            if not indices:
                QMessageBox.warning(self, "Aviso", f"Nenhuma página válida encontrada no intervalo informado. O documento possui {self.total_paginas_dividir} páginas.")
                return

            saida, _ = QFileDialog.getSaveFileName(self, "Salvar Páginas Extraídas", "paginas_extraidas.pdf", "PDF (*.pdf)")
            if saida:
                self.iniciar_tarefa(OperacoesPDF.extrair_intervalo, self.caminho_pdf_dividir, saida, indices)

    def interpretar_intervalo(self, texto: str, max_paginas: int) -> list[int]:
        indices = set()
        partes = [p.strip() for p in texto.split(",") if p.strip()]
        for parte in partes:
            if "-" in parte:
                sub = parte.split("-")
                if len(sub) == 2 and sub[0].strip().isdigit() and sub[1].strip().isdigit():
                    inicio = max(1, int(sub[0].strip()))
                    fim = min(max_paginas, int(sub[1].strip()))
                    for p in range(inicio, fim + 1):
                        indices.add(p - 1)
            elif parte.isdigit():
                num = int(parte)
                if 1 <= num <= max_paginas:
                    indices.add(num - 1)
        return sorted(list(indices))

    def criar_aba_organizar(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(14)

        linha_selecao = QHBoxLayout()
        self.botao_selecionar_organizar = QPushButton("Selecionar PDF")
        self.botao_selecionar_organizar.clicked.connect(self.selecionar_pdf_organizar)
        self.rotulo_pdf_organizar = QLabel("Nenhum PDF selecionado")
        self.rotulo_pdf_organizar.setStyleSheet("color: #7A7469; font-style: italic;")
        linha_selecao.addWidget(self.botao_selecionar_organizar)
        linha_selecao.addWidget(self.rotulo_pdf_organizar, 1)
        layout.addLayout(linha_selecao)

        cartao_rotacao = QFrame()
        cartao_rotacao.setObjectName("Cartao")
        layout_rotacao = QVBoxLayout(cartao_rotacao)
        layout_rotacao.setSpacing(12)

        rotulo_titulo_rotacao = QLabel("Opções de Rotação:")
        rotulo_titulo_rotacao.setStyleSheet("font-weight: bold;")
        layout_rotacao.addWidget(rotulo_titulo_rotacao)

        linha_alvo = QHBoxLayout()
        self.radio_todas_paginas = QRadioButton("Aplicar em todas as páginas")
        self.radio_todas_paginas.setChecked(True)
        self.radio_uma_pagina = QRadioButton("Apenas na página:")
        self.spin_pagina_organizar = QSpinBox()
        self.spin_pagina_organizar.setRange(1, 1)
        self.spin_pagina_organizar.setEnabled(False)
        self.radio_uma_pagina.toggled.connect(self.spin_pagina_organizar.setEnabled)

        linha_alvo.addWidget(self.radio_todas_paginas)
        linha_alvo.addWidget(self.radio_uma_pagina)
        linha_alvo.addWidget(self.spin_pagina_organizar)
        linha_alvo.addStretch()
        layout_rotacao.addLayout(linha_alvo)

        linha_botoes = QHBoxLayout()
        self.botao_rot_90h = QPushButton("Girar 90° Horário")
        self.botao_rot_90h.clicked.connect(lambda: self.executar_rotacao(90))

        self.botao_rot_90ah = QPushButton("Girar 90° Anti-horário")
        self.botao_rot_90ah.clicked.connect(lambda: self.executar_rotacao(270))

        self.botao_rot_180 = QPushButton("Girar 180°")
        self.botao_rot_180.clicked.connect(lambda: self.executar_rotacao(180))

        linha_botoes.addWidget(self.botao_rot_90h)
        linha_botoes.addWidget(self.botao_rot_90ah)
        linha_botoes.addWidget(self.botao_rot_180)
        layout_rotacao.addLayout(linha_botoes)

        layout.addWidget(cartao_rotacao)
        layout.addStretch()

        return widget

    def selecionar_pdf_organizar(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF", "", "Documentos PDF (*.pdf)")
        if caminho:
            self.caminho_pdf_organizar = caminho
            try:
                informacoes = OperacoesPDF.obter_informacoes(caminho)
                self.rotulo_pdf_organizar.setText(f"{informacoes['nome_arquivo']} ({informacoes['total_paginas']} páginas)")
                self.rotulo_pdf_organizar.setStyleSheet("color: #2C2926; font-weight: bold;")
                self.spin_pagina_organizar.setRange(1, informacoes['total_paginas'])
            except Exception:
                self.rotulo_pdf_organizar.setText(os.path.basename(caminho))

    def executar_rotacao(self, angulo: int):
        if not self.caminho_pdf_organizar:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo PDF primeiro.")
            return

        saida, _ = QFileDialog.getSaveFileName(self, "Salvar PDF Rotacionado", "documento_rotacionado.pdf", "PDF (*.pdf)")
        if not saida:
            return

        if self.radio_todas_paginas.isChecked():
            self.iniciar_tarefa(OperacoesPDF.rotacionar_todas, self.caminho_pdf_organizar, saida, angulo)
        else:
            numero_pagina = self.spin_pagina_organizar.value() - 1
            self.iniciar_tarefa(OperacoesPDF.rotacionar_pagina, self.caminho_pdf_organizar, saida, numero_pagina, angulo)

    def iniciar_tarefa(self, funcao, *argumentos):
        self.abas.setEnabled(False)
        self.barra_progresso.show()
        self.barra_progresso.setRange(0, 100)
        self.barra_progresso.setValue(10)
        self.rotulo_status.setText("Processando alterações no documento...")

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
        if isinstance(resultado, list):
            mensagem = f"Operação concluída! {len(resultado)} páginas geradas com sucesso."
        else:
            mensagem = f"Arquivo gerado com sucesso!\nSalvo em: {resultado}"
        self.rotulo_status.setText(mensagem)
        QMessageBox.information(self, "Sucesso", mensagem)

    def ao_erro(self, mensagem_erro: str):
        self.barra_progresso.hide()
        self.abas.setEnabled(True)
        self.rotulo_status.setText("Erro ao executar operação.")
        QMessageBox.critical(self, "Erro no Editor", f"Ocorreu um erro durante a operação:\n\n{mensagem_erro}")

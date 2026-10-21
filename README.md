# Convedit — Editor e Conversor Profissional de Documentos

O **Convedit** é uma aplicação desktop de alta performance desenvolvida em **Python** e **PySide6 (Qt6)** para manipulação avançada, conversão multiformato, higienização documental em conformidade com a LGPD, comparação visual de versões e compressão otimizada de arquivos digitais.

Projetada com arquitetura modular, execução em segundo plano não bloqueante (`QThread`) e gerenciamento seguro de descritores de arquivo, a aplicação atende tanto a fluxos corporativos quanto jurídicos e editoriais.

---

## Funcionalidades

### 1. Conversor Inteligente Multiformato
- **Conversão de PDF:** Exportação para Microsoft Word (`.docx`), Markdown (`.md`), Texto puro (`.txt`) e extração em lote de páginas como imagens (`.png` a 300 DPI).
- **Conversão de Documentos Word:** Exportação direta de `.docx` para PDF, HTML estruturado, Markdown e Texto.
- **Manipulação de Imagens:** Conversão individual ou compilação de múltiplos arquivos gráficos (`.png`, `.jpg`, `.jpeg`) em documento PDF consolidado.
- **Tabelas e Dados:** Conversão bidirecional entre planilhas Excel (`.xlsx`) e arquivos CSV, além de exportação de objetos JSON tabulares.

### 2. Editor Profissional de PDF
- **Mesclagem de Documentos (Merge):** Junção de múltiplos arquivos PDF com fila reordenável, detecção de metadados e contagem de páginas.
- **Divisão e Extração (Split):** Separação integral de páginas ou extração seletiva baseada em intervalos customizados (ex: `1-3, 5, 8-10`).
- **Organização e Rotação:** Ajuste de orientação de páginas individuais ou em lote (90° horário, 90° anti-horário e 180°).

### 3. Higienização e Proteção (Conformidade LGPD)
- **Redação Física Permanente:** Destruição real e definitiva de dados sensíveis na árvore interna do PDF via `apply_redactions` com coleta profunda de lixo (`garbage=3`), impedindo extração por leitores de tela ou engenharia reversa.
- **Detecção Automatizada:** Expressões regulares otimizadas para identificação e censura imediata de CPFs, e-mails e números de telefone.
- **Higienização Nominal:** Suporte a termos e palavras-chave adicionais informadas pelo operador (nomes de partes, números de conta, valores sigilosos).
- **Marcas d'Água:** Inserção em lote de marcações corporativas de confidencialidade em todas as páginas.

### 4. Comparador Visual de Documentos (Diff Tool)
- **Detecção de Divergências:** Algoritmo de subtração diferencial gráfica (`ImageChops`) que destaca alterações entre versões do mesmo documento em vermelho sobreposto ao leiaute original.
- **Navegador Página a Página:** Inspeção visual com modos de exibição em mapa de calor (*Diff*) ou comparação sincronizada lado a lado (*Side by Side*).
- **Relatório de Auditoria:** Exportação automatizada de todas as páginas divergentes em imagens PNG de alta fidelidade.

### 5. Compressão Otimizada
- **Redução Estrutural:** Compactação de fluxos de conteúdo, remoção de objetos duplicados e descarte de recursos órfãos.
- **Níveis Selecionáveis:** Perfis de compressão *Leve*, *Equilibrado* (recomendado para anexos de e-mail) e *Máximo*.
- **Relatório de Eficiência:** Métricas exibindo tamanho inicial, tamanho final, bytes economizados e percentual de redução obtido.

---

## Tecnologias e Bibliotecas

| Componente | Tecnologia | Finalidade |
| :--- | :--- | :--- |
| **Linguagem** | Python 3.10+ | Linguagem central de desenvolvimento |
| **Interface Gráfica** | PySide6 (Qt 6.7) | Widgets desktop nativos e estilização QSS unificada |
| **Motor de PDF** | PyMuPDF (fitz) | Renderização, manipulação estrutural, rotação e redação |
| **Processamento de Imagem** | Pillow (PIL) | Análise diferencial de pixels e conversão gráfica |
| **Conversão de Documentos** | pdf2docx / docx2pdf / python-docx / mammoth | Conversão e parsing de formatos do Microsoft Word |
| **Manipulação de Dados** | pandas / openpyxl | Leitura e escrita de arquivos CSV, Excel e JSON |
| **Empacotamento** | PyInstaller | Criação de binários executáveis autônomos para Windows |

---

## Arquitetura do Projeto

```text
ConvEdit App/
├── conversores/             # Motores de conversão multiformato (PDF, Word, Imagens, Dados)
│   ├── converter_dados.py
│   ├── converter_imagem.py
│   ├── converter_pdf.py
│   └── converter_word.py
├── editor/                  # Motores de manipulação e análise de arquivos PDF
│   ├── comparador_pdf.py
│   ├── compressao_pdf.py
│   ├── operacoes_pdf.py
│   └── redacao_pdf.py
├── interface/               # Camada de apresentação em PySide6
│   ├── componentes/         # Componentes transversais (tarefas assíncronas em segundo plano)
│   │   └── trabalhador.py
│   ├── telas/               # Telas modulares de cada recurso da aplicação
│   │   ├── tela_base.py
│   │   ├── tela_comparador.py
│   │   ├── tela_compressor.py
│   │   ├── tela_conversor.py
│   │   ├── tela_editor.py
│   │   └── tela_protecao.py
│   ├── tela_principal.py    # Janela principal, barra lateral e gerenciador de telas
│   └── tema_cores.py        # Folha de estilos unificada (QSS)
├── principal.py             # Ponto de entrada (Entry-Point) da aplicação
├── requirements.txt         # Especificação de dependências do ambiente
├── .gitignore               # Regras de exclusão de artefatos para o Git
└── README.md                # Documentação técnica do projeto
```

---

## Instalação e Execução

### 1. Clonar o Repositório
```bash
git clone https://github.com/Magnao0507/ConvEdit-App.git
cd ConvEdit-App
```

### 2. Criar e Ativar o Ambiente Virtual
No Windows (Prompt de Comando ou PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Instalar as Dependências
```powershell
pip install -r requirements.txt
```

### 4. Executar a Aplicação
```powershell
python principal.py
```

---

## Como Gerar o Executável (.exe)

O projeto está configurado para empacotamento com o **PyInstaller**. Certifique-se de estar com o ambiente virtual ativo:

```powershell
pip install pyinstaller
```

### Opção 1: Pasta Única (Recomendado — inicialização imediata)
```powershell
pyinstaller --noconfirm --onedir --windowed --name "Convedit" "principal.py"
```
O executável e seus recursos estarão na pasta `dist/Convedit/Convedit.exe`.

### Opção 2: Arquivo Único Standalone (.exe portátil)
```powershell
pyinstaller --noconfirm --onefile --windowed --name "Convedit" "principal.py"
```
O arquivo único será gerado diretamente em `dist/Convedit.exe`.

---

## Autoria

Desenvolvido por **Arthur Magno**.
Projeto disponibilizado sob licença de uso para fins profissionais e de portfólio.

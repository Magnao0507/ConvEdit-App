# Convedit

O **Convedit** é um editor e conversor de documentos desktop que criei em Python usando PySide6 (Qt6). O objetivo principal dele é ser uma ferramenta prática para o dia a dia para lidar com arquivos PDF, Word, imagens e planilhas, reunindo várias utilidades em um só lugar sem depender de ferramentas online ou pagas.

---

## O que ele faz?

- **Conversor Multiformato:** Converte arquivos entre PDF, Word (`.docx`), Markdown, Texto (`.txt`), imagens (`.png`, `.jpg`) e planilhas (Excel e CSV).
- **Editor de PDF Completo:** Permite juntar vários PDFs, dividir páginas, extrair intervalos específicos e girar páginas de uma só vez.
- **Higienização e LGPD:** Remove dados de documentos (como CPFs, e-mails e telefones) com tarjas pretas.
- **Comparador Visual:** Compara duas versões de um PDF lado a lado ou mostrando as diferenças destacadas em vermelho.
- **Compressão de PDF:** Reduz o tamanho de PDFs pesados, com opções de níveis leve, equilibrado e máximo.

---

## Requisitos para Funcionamento

Para conseguir rodar o Convedit na sua máquina, você vai precisar ter instalado:

1. **Python (versão 3.10 ou superior):** Certifique-se de marcar a opção de adicionar o Python ao PATH do sistema durante a instalação.
2. **Gerenciador de Pacotes Pip:** Geralmente já vem instalado junto com o Python.
3. **Microsoft Word (Opcional):** Necessário apenas se você for utilizar a conversão de arquivos `.docx` para PDF, pois o utilitário interno utiliza a automação do Office no Windows.

---

## Como instalar e rodar o projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/Magnao0507/ConvEdit-App.git](https://github.com/Magnao0507/ConvEdit-App.git)
   cd ConvEdit-App

```

2. **Crie e ative um ambiente virtual:**
```bash
python -m venv .venv
.venv\Scripts\activate

```


3. **Instale as dependências:**
```bash
pip install -r requirements.txt

```


4. **Inicie a aplicação:**
```bash
python principal.py

```



---

## Gerando o executável (.exe)

Se você quiser transformar o projeto em um executável para rodar direto no Windows sem precisar abrir o terminal, você pode usar o PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name "Convedit" "principal.py"

```

O arquivo final vai aparecer dentro da pasta `dist/`.
 
---

## Licença

Desenvolvido por **Arthur Magno**. Sinta-se à vontade para usar e estudar o código!

```

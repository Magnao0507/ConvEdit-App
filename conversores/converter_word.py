import docx
import mammoth
from docx2pdf import convert as docx_para_pdf

class ConversorWord:
    @staticmethod
    def para_pdf(caminho_word: str, caminho_saida: str) -> str:
        """Converte documento Word (.docx) para PDF mantendo layout original."""
        try:
            docx_para_pdf(caminho_word, caminho_saida)
        except Exception as erro:
            raise RuntimeError(
                "A conversão direta de Word para PDF depende do Microsoft Word instalado no sistema. "
                f"Verifique se o Word está instalado e acessível. Detalhes: {str(erro)}"
            ) from erro
        return caminho_saida

    @staticmethod
    def para_html(caminho_word: str, caminho_saida: str) -> str:
        """Converte documento Word (.docx) para página HTML."""
        with open(caminho_word, "rb") as arquivo_docx:
            resultado = mammoth.convert_to_html(arquivo_docx)
            codigo_html = resultado.value

        with open(caminho_saida, "w", encoding="utf-8") as arquivo_html:
            arquivo_html.write(codigo_html)
        return caminho_saida

    @staticmethod
    def para_markdown(caminho_word: str, caminho_saida: str) -> str:
        """Converte documento Word (.docx) para formato Markdown (.md)."""
        with open(caminho_word, "rb") as arquivo_docx:
            resultado = mammoth.convert_to_markdown(arquivo_docx)
            codigo_markdown = resultado.value

        with open(caminho_saida, "w", encoding="utf-8") as arquivo_md:
            arquivo_md.write(codigo_markdown)
        return caminho_saida

    @staticmethod
    def para_texto(caminho_word: str, caminho_saida: str) -> str:
        """Extrai o texto puro de um documento Word (.docx)."""
        documento = docx.Document(caminho_word)
        paragrafos = [paragrafo.text for paragrafo in documento.paragraphs]

        with open(caminho_saida, "w", encoding="utf-8") as arquivo_texto:
            arquivo_texto.write("\n".join(paragrafos))
        return caminho_saida

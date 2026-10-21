import os
import fitz
from pdf2docx import Converter

class ConversorPDF:
    @staticmethod
    def para_word(caminho_pdf: str, caminho_saida: str) -> str:
        """Converte documento PDF para Microsoft Word (.docx)."""
        conversor = Converter(caminho_pdf)
        try:
            conversor.convert(caminho_saida, start=0, end=None)
        finally:
            conversor.close()
        return caminho_saida

    @staticmethod
    def para_imagens(caminho_pdf: str, pasta_saida: str, formato: str = "png", em_lote: bool = True) -> list[str]:
        """Extrai as páginas do PDF como arquivos de imagem de alta resolução (300 DPI)."""
        caminhos_salvos = []
        nome_base = os.path.splitext(os.path.basename(caminho_pdf))[0]

        with fitz.open(caminho_pdf) as documento:
            total_paginas = len(documento)
            for numero_pagina in range(total_paginas):
                pagina = documento.load_page(numero_pagina)
                mapa_pixels = pagina.get_pixmap(dpi=300)
                caminho_imagem = os.path.join(pasta_saida, f"{nome_base}_pagina_{numero_pagina + 1}.{formato}")
                mapa_pixels.save(caminho_imagem)
                caminhos_salvos.append(caminho_imagem)

                if not em_lote:
                    break

        return caminhos_salvos

    @staticmethod
    def para_texto(caminho_pdf: str, caminho_saida: str) -> str:
        """Extrai o texto puro de um documento PDF."""
        with fitz.open(caminho_pdf) as documento:
            texto_completo = [pagina.get_text() for pagina in documento]

        with open(caminho_saida, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(texto_completo))
        return caminho_saida

    @staticmethod
    def para_markdown(caminho_pdf: str, caminho_saida: str) -> str:
        """Converte o texto estruturado do PDF em formato Markdown (.md)."""
        texto_markdown = []
        with fitz.open(caminho_pdf) as documento:
            for pagina in documento:
                try:
                    texto_markdown.append(pagina.get_text("markdown"))
                except ValueError:
                    texto_markdown.append(pagina.get_text())

        with open(caminho_saida, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n\n".join(texto_markdown))
        return caminho_saida

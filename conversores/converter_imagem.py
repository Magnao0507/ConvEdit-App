import fitz
from PIL import Image

class ConversorImagem:
    @staticmethod
    def para_pdf(lista_imagens: list[str], caminho_saida: str) -> str:
        """Combina uma ou mais imagens em um único documento PDF."""
        documento_pdf = fitz.open()

        try:
            for caminho_imagem in lista_imagens:
                with fitz.open(caminho_imagem) as imagem_fitz:
                    retangulo = imagem_fitz[0].rect
                    bytes_pdf = imagem_fitz.convert_to_pdf()

                with fitz.open("pdf", bytes_pdf) as pdf_temporario:
                    nova_pagina = documento_pdf.new_page(width=retangulo.width, height=retangulo.height)
                    nova_pagina.show_pdf_page(retangulo, pdf_temporario, 0)

            documento_pdf.save(caminho_saida)
        finally:
            documento_pdf.close()

        return caminho_saida

    @staticmethod
    def converter_formato(caminho_imagem: str, caminho_saida: str, formato_saida: str) -> str:
        """Converte uma imagem para outro formato gráfico (ex: PNG para JPEG)."""
        with Image.open(caminho_imagem) as imagem_pil:
            if formato_saida.upper() in ["JPG", "JPEG"] and imagem_pil.mode in ("RGBA", "P"):
                imagem_pil = imagem_pil.convert("RGB")
            imagem_pil.save(caminho_saida, format=formato_saida.upper())
        return caminho_saida

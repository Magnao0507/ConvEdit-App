import io
import os
import fitz
from PIL import Image, ImageChops

class ComparadorVisual:
    @staticmethod
    def renderizar_pagina(caminho_pdf: str, numero_pagina: int, dpi: int = 120) -> bytes | None:
        """Renderiza uma página específica do PDF e retorna os bytes em formato PNG."""
        with fitz.open(caminho_pdf) as documento:
            if numero_pagina < 0 or numero_pagina >= len(documento):
                return None
            pagina = documento.load_page(numero_pagina)
            mapa_pixels = pagina.get_pixmap(dpi=dpi)
            return mapa_pixels.tobytes("png")

    @staticmethod
    def gerar_imagem_diff(caminho_pdf1: str, caminho_pdf2: str, numero_pagina: int, dpi: int = 130) -> tuple[bytes | None, bool]:
        """
        Compara a mesma página de dois arquivos PDF e retorna uma imagem com mapa
        de diferenças em vermelho, acompanhada de um indicador booleano de divergência.
        """
        with fitz.open(caminho_pdf1) as documento1, fitz.open(caminho_pdf2) as documento2:
            total1, total2 = len(documento1), len(documento2)

            if numero_pagina >= total1 and numero_pagina >= total2:
                return None, False

            if numero_pagina >= total1:
                pagina2 = documento2.load_page(numero_pagina)
                mapa_pixels = pagina2.get_pixmap(dpi=dpi)
                return mapa_pixels.tobytes("png"), True

            if numero_pagina >= total2:
                pagina1 = documento1.load_page(numero_pagina)
                mapa_pixels = pagina1.get_pixmap(dpi=dpi)
                return mapa_pixels.tobytes("png"), True

            pagina1 = documento1.load_page(numero_pagina)
            pagina2 = documento2.load_page(numero_pagina)

            mapa_pixels1 = pagina1.get_pixmap(dpi=dpi)
            mapa_pixels2 = pagina2.get_pixmap(dpi=dpi)

            imagem1 = Image.frombytes("RGB", [mapa_pixels1.width, mapa_pixels1.height], mapa_pixels1.samples)
            imagem2 = Image.frombytes("RGB", [mapa_pixels2.width, mapa_pixels2.height], mapa_pixels2.samples)

        if imagem1.size != imagem2.size:
            imagem2 = imagem2.resize(imagem1.size)

        diferenca = ImageChops.difference(imagem1, imagem2)
        diferenca_cinza = diferenca.convert("L")

        limiar = 15
        houve_alteracao = any(pixel > limiar for pixel in diferenca_cinza.getdata())

        mascara = diferenca_cinza.point(lambda valor: 255 if valor > limiar else 0)

        imagem1_suave = imagem1.copy()
        imagem1_suave.putalpha(110)

        imagem_base = Image.new("RGBA", imagem1.size, (255, 255, 255, 255))
        imagem_base.paste(imagem1_suave, (0, 0), imagem1_suave)

        camada_vermelha = Image.new("RGBA", imagem1.size, (230, 40, 40, 180))
        imagem_base.paste(camada_vermelha, (0, 0), mascara)

        buffer_memoria = io.BytesIO()
        imagem_base.convert("RGB").save(buffer_memoria, format="PNG")
        return buffer_memoria.getvalue(), houve_alteracao

    @staticmethod
    def comparar_pagina(caminho_pdf1: str, caminho_pdf2: str, numero_pagina: int, caminho_saida: str) -> str | None:
        """Salva a imagem de diferença entre duas páginas em um arquivo PNG."""
        bytes_imagem, _ = ComparadorVisual.gerar_imagem_diff(caminho_pdf1, caminho_pdf2, numero_pagina)
        if bytes_imagem:
            with open(caminho_saida, "wb") as arquivo:
                arquivo.write(bytes_imagem)
            return caminho_saida
        return None

    @staticmethod
    def comparar_documento_completo(caminho_pdf1: str, caminho_pdf2: str, pasta_saida: str, callback_progresso=None) -> list[str]:
        """Compara todas as páginas de dois PDFs e exporta as imagens das diferenças para uma pasta."""
        with fitz.open(caminho_pdf1) as documento1, fitz.open(caminho_pdf2) as documento2:
            total_paginas = max(len(documento1), len(documento2))

        imagens_diferencas = []
        for indice in range(total_paginas):
            if callback_progresso:
                callback_progresso(
                    int((indice / total_paginas) * 100),
                    f"Comparando página {indice + 1} de {total_paginas}..."
                )

            caminho_saida = os.path.join(pasta_saida, f"diferenca_pagina_{indice + 1}.png")
            resultado = ComparadorVisual.comparar_pagina(caminho_pdf1, caminho_pdf2, indice, caminho_saida)
            if resultado:
                imagens_diferencas.append(resultado)

        if callback_progresso:
            callback_progresso(100, "Comparação de todas as páginas concluída!")

        return imagens_diferencas

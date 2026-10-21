import os
import shutil
import tempfile
import fitz

class CompressorPDF:
    @staticmethod
    def comprimir_pdf(caminho_entrada: str, caminho_saida: str, nivel: str = "equilibrado", callback_progresso=None) -> dict:
        """
        Otimiza a estrutura do PDF reduzindo tamanho por meio de coleta de lixo,
        desinflação e limpeza de fluxos de dados.
        """
        if callback_progresso:
            callback_progresso(20, "Abrindo documento e analisando fluxos...")

        diretorio_saida = os.path.dirname(os.path.abspath(caminho_saida))
        descritor, caminho_temporario = tempfile.mkstemp(suffix=".pdf", dir=diretorio_saida)
        os.close(descritor)

        with fitz.open(caminho_entrada) as documento:
            if callback_progresso:
                callback_progresso(50, f"Aplicando otimização nível '{nivel}'...")

            if nivel == "leve":
                documento.save(
                    caminho_temporario,
                    garbage=3,
                    deflate=True
                )
            elif nivel == "maximo":
                documento.save(
                    caminho_temporario,
                    garbage=4,
                    deflate=True,
                    clean=True,
                    deflate_images=True,
                    deflate_fonts=True
                )
            else:
                documento.save(
                    caminho_temporario,
                    garbage=4,
                    deflate=True,
                    clean=True
                )

        if callback_progresso:
            callback_progresso(90, "Calculando métricas de redução...")

        shutil.move(caminho_temporario, caminho_saida)

        tamanho_original = os.path.getsize(caminho_entrada)
        novo_tamanho = os.path.getsize(caminho_saida)
        bytes_salvos = max(0, tamanho_original - novo_tamanho)
        proporcao = round((bytes_salvos / tamanho_original) * 100, 2) if tamanho_original > 0 else 0.0

        if callback_progresso:
            callback_progresso(100, "Compressão concluída com sucesso!")

        return {
            "caminho_saida": caminho_saida,
            "tamanho_original": tamanho_original,
            "novo_tamanho": novo_tamanho,
            "bytes_salvos": bytes_salvos,
            "proporcao": proporcao
        }

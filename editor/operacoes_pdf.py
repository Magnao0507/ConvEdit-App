import os
import shutil
import tempfile
import fitz

class OperacoesPDF:
    @staticmethod
    def obter_informacoes(caminho_pdf: str) -> dict:
        """Retorna informações estruturais e contagem de páginas do PDF."""
        with fitz.open(caminho_pdf) as documento:
            total_paginas = len(documento)
            
        tamanho_bytes = os.path.getsize(caminho_pdf)
        tamanho_mb = tamanho_bytes / (1024 * 1024)
        formato_tamanho = f"{tamanho_mb:.2f} MB" if tamanho_mb >= 1 else f"{tamanho_bytes / 1024:.1f} KB"
        
        return {
            "total_paginas": total_paginas,
            "tamanho_bytes": tamanho_bytes,
            "tamanho_formatado": formato_tamanho,
            "nome_arquivo": os.path.basename(caminho_pdf)
        }

    @staticmethod
    def mesclar(lista_caminhos_pdf: list[str], caminho_saida: str, callback_progresso=None) -> str:
        """Combina múltiplos arquivos PDF em um único documento."""
        total_arquivos = len(lista_caminhos_pdf)
        diretorio = os.path.dirname(os.path.abspath(caminho_saida))
        descritor, caminho_temporario = tempfile.mkstemp(suffix=".pdf", dir=diretorio)
        os.close(descritor)

        with fitz.open() as documento_final:
            for indice, caminho in enumerate(lista_caminhos_pdf):
                if callback_progresso:
                    callback_progresso(int((indice / total_arquivos) * 90), f"Processando: {os.path.basename(caminho)}")
                with fitz.open(caminho) as documento_atual:
                    documento_final.insert_pdf(documento_atual)
                    
            if callback_progresso:
                callback_progresso(95, "Salvando arquivo consolidado...")
            documento_final.save(caminho_temporario)

        shutil.move(caminho_temporario, caminho_saida)
            
        if callback_progresso:
            callback_progresso(100, "Concluído com sucesso!")
        return caminho_saida

    @staticmethod
    def dividir(caminho_pdf: str, pasta_saida: str, callback_progresso=None) -> list[str]:
        """Divide todas as páginas de um PDF em arquivos individuais."""
        nome_base = os.path.splitext(os.path.basename(caminho_pdf))[0]
        caminhos_salvos = []
        
        with fitz.open(caminho_pdf) as documento:
            total_paginas = len(documento)
            for numero_pagina in range(total_paginas):
                if callback_progresso:
                    callback_progresso(int((numero_pagina / total_paginas) * 100), f"Extraindo página {numero_pagina + 1} de {total_paginas}...")
                
                caminho_pagina = os.path.join(pasta_saida, f"{nome_base}_pagina_{numero_pagina + 1}.pdf")
                descritor, caminho_temporario = tempfile.mkstemp(suffix=".pdf", dir=pasta_saida)
                os.close(descritor)
                
                with fitz.open() as novo_documento:
                    novo_documento.insert_pdf(documento, from_page=numero_pagina, to_page=numero_pagina)
                    novo_documento.save(caminho_temporario)
                    
                shutil.move(caminho_temporario, caminho_pagina)
                caminhos_salvos.append(caminho_pagina)
                
        if callback_progresso:
            callback_progresso(100, "Extração concluída!")
        return caminhos_salvos

    @staticmethod
    def extrair_intervalo(caminho_pdf: str, caminho_saida: str, indices_paginas: list[int]) -> str:
        """Extrai páginas selecionadas e gera um novo documento PDF."""
        diretorio = os.path.dirname(os.path.abspath(caminho_saida))
        descritor, caminho_temporario = tempfile.mkstemp(suffix=".pdf", dir=diretorio)
        os.close(descritor)

        with fitz.open(caminho_pdf) as documento:
            with fitz.open() as novo_documento:
                for indice in indices_paginas:
                    if 0 <= indice < len(documento):
                        novo_documento.insert_pdf(documento, from_page=indice, to_page=indice)
                novo_documento.save(caminho_temporario)

        shutil.move(caminho_temporario, caminho_saida)
        return caminho_saida

    @staticmethod
    def rotacionar_pagina(caminho_pdf: str, caminho_saida: str, numero_pagina: int, angulo: int = 90) -> str:
        """Aplica rotação a uma página específica do PDF."""
        diretorio = os.path.dirname(os.path.abspath(caminho_saida))
        descritor, caminho_temporario = tempfile.mkstemp(suffix=".pdf", dir=diretorio)
        os.close(descritor)

        with fitz.open(caminho_pdf) as documento:
            if 0 <= numero_pagina < len(documento):
                pagina = documento[numero_pagina]
                rotacao_atual = pagina.rotation
                pagina.set_rotation((rotacao_atual + angulo) % 360)
            documento.save(caminho_temporario)

        shutil.move(caminho_temporario, caminho_saida)
        return caminho_saida

    @staticmethod
    def rotacionar_todas(caminho_pdf: str, caminho_saida: str, angulo: int = 90) -> str:
        """Aplica rotação a todas as páginas do documento PDF."""
        diretorio = os.path.dirname(os.path.abspath(caminho_saida))
        descritor, caminho_temporario = tempfile.mkstemp(suffix=".pdf", dir=diretorio)
        os.close(descritor)

        with fitz.open(caminho_pdf) as documento:
            for pagina in documento:
                pagina.set_rotation((pagina.rotation + angulo) % 360)
            documento.save(caminho_temporario)

        shutil.move(caminho_temporario, caminho_saida)
        return caminho_saida

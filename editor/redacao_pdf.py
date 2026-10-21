import os
import re
import shutil
import tempfile
import fitz

class ManipuladorRedacao:
    PADRAO_CPF = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'
    PADRAO_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    PADRAO_TELEFONE = r'\b(?:\+55\s?)?(?:\(?\d{2}\)?[\s-]?)?\d{4,5}-?\d{4}\b'

    @staticmethod
    def higienizar_documento(
        caminho_pdf: str,
        caminho_saida: str,
        termos: list[str] | None = None,
        censurar_cpf: bool = True,
        censurar_email: bool = True,
        censurar_telefone: bool = True,
        texto_tarja: str = "[DADO PROTEGIDO]",
        callback_progresso=None
    ) -> dict:
        """
        Localiza dados pessoais e termos sensíveis em todas as páginas,
        aplicando redação física permanente em conformidade com a LGPD.
        """
        diretorio_saida = os.path.dirname(os.path.abspath(caminho_saida))
        descritor, caminho_temporario = tempfile.mkstemp(suffix=".pdf", dir=diretorio_saida)
        os.close(descritor)

        total_redacoes = 0
        paginas_afetadas = set()
        termos_processados = [termo.strip() for termo in (termos or []) if termo.strip()]

        with fitz.open(caminho_pdf) as documento:
            total_paginas = len(documento)

            for numero_pagina in range(total_paginas):
                if callback_progresso:
                    callback_progresso(
                        int((numero_pagina / total_paginas) * 80),
                        f"Analisando página {numero_pagina + 1} de {total_paginas}..."
                    )

                pagina = documento[numero_pagina]
                retangulos_para_redigir = []

                for termo in termos_processados:
                    for ocorrencia_retangulo in pagina.search_for(termo):
                        retangulos_para_redigir.append(ocorrencia_retangulo)

                if censurar_cpf or censurar_email or censurar_telefone:
                    texto_pagina = pagina.get_text("text")

                    padroes_ativos = []
                    if censurar_cpf:
                        padroes_ativos.append(ManipuladorRedacao.PADRAO_CPF)
                    if censurar_email:
                        padroes_ativos.append(ManipuladorRedacao.PADRAO_EMAIL)
                    if censurar_telefone:
                        padroes_ativos.append(ManipuladorRedacao.PADRAO_TELEFONE)

                    for padrao in padroes_ativos:
                        for ocorrencia in re.finditer(padrao, texto_pagina):
                            trecho = ocorrencia.group(0).strip()
                            if trecho:
                                for ocorrencia_retangulo in pagina.search_for(trecho):
                                    retangulos_para_redigir.append(ocorrencia_retangulo)

                for retangulo in retangulos_para_redigir:
                    pagina.add_redact_annot(
                        retangulo,
                        text=texto_tarja,
                        fill=(0, 0, 0),
                        fontname="helv",
                        fontsize=8
                    )
                    total_redacoes += 1
                    paginas_afetadas.add(numero_pagina + 1)

                if retangulos_para_redigir:
                    pagina.apply_redactions()

            if callback_progresso:
                callback_progresso(90, "Finalizando gravação do documento higienizado...")

            documento.save(caminho_temporario, garbage=3, deflate=True)

        shutil.move(caminho_temporario, caminho_saida)

        if callback_progresso:
            callback_progresso(100, "Concluído com sucesso!")

        return {
            "caminho_saida": caminho_saida,
            "total_redacoes": total_redacoes,
            "paginas_afetadas": sorted(list(paginas_afetadas))
        }

    @staticmethod
    def adicionar_marca_dagua(caminho_pdf: str, caminho_saida: str, texto_marca: str = "CONFIDENCIAL") -> str:
        """Insere marca d'água diagonal em todas as páginas do documento."""
        diretorio_saida = os.path.dirname(os.path.abspath(caminho_saida))
        descritor, caminho_temporario = tempfile.mkstemp(suffix=".pdf", dir=diretorio_saida)
        os.close(descritor)

        with fitz.open(caminho_pdf) as documento:
            for pagina in documento:
                retangulo = pagina.rect
                ponto_central = fitz.Point(retangulo.width / 4, retangulo.height / 2)
                pagina.insert_text(ponto_central, texto_marca, fontsize=48, rotate=0, color=(0.7, 0.7, 0.7))

            documento.save(caminho_temporario, garbage=3, deflate=True)

        shutil.move(caminho_temporario, caminho_saida)
        return caminho_saida

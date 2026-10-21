import pandas as pd

class ConversorDados:
    @staticmethod
    def csv_para_excel(caminho_csv: str, caminho_saida: str) -> str:
        """Converte arquivo CSV para planilha Excel (.xlsx)."""
        tabela = pd.read_csv(caminho_csv)
        tabela.to_excel(caminho_saida, index=False)
        return caminho_saida

    @staticmethod
    def excel_para_csv(caminho_excel: str, caminho_saida: str) -> str:
        """Converte planilha Excel (.xlsx) para arquivo CSV."""
        tabela = pd.read_excel(caminho_excel)
        tabela.to_csv(caminho_saida, index=False)
        return caminho_saida

    @staticmethod
    def json_para_csv(caminho_json: str, caminho_saida: str) -> str:
        """Converte arquivo JSON para formato tabular CSV."""
        tabela = pd.read_json(caminho_json)
        tabela.to_csv(caminho_saida, index=False)
        return caminho_saida

    @staticmethod
    def json_para_excel(caminho_json: str, caminho_saida: str) -> str:
        """Converte arquivo JSON para planilha Excel (.xlsx)."""
        tabela = pd.read_json(caminho_json)
        tabela.to_excel(caminho_saida, index=False)
        return caminho_saida

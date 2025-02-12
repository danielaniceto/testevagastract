from flask import Response
import requests
import io
import csv

AUTH_TOKEN = "Bearer ProcessoSeletivoStract2025"
BASE_URL = "https://sidebar.stract.to/api/accounts"

class ControllerCandidato:
    def dados_candidato():
        return {
                "nome": "Daniel Gustavo Aniceto",
                "email": "danielgustavots@gmail.com",
                "linkedin": "https://www.linkedin.com/in/daniel-gustavo-aniceto-63908710b/"
            }
    
class ControllerPlataforma:
    @staticmethod
    def get_insights_by_platform(platform):
        """Obtém os insights de anúncios de uma plataforma específica"""

        url_accounts = f"{BASE_URL}/accounts?platform={platform}"
        response_accounts = requests.get(url_accounts, headers={"Authorization": f'Bearer {AUTH_TOKEN}'})

        if response_accounts.status_code != 200:
            return {"error": "Erro ao buscar contas da plataforma"}

        accounts_data = response_accounts.json()

        insights_data = []

        for account in accounts_data.get("accounts", []):
            account_name = account.get("name", "Desconhecido")

            url_insights = f"{BASE_URL}/insights?platform={platform}&account={account_name}&token={AUTH_TOKEN}"
            response_insights = requests.get(url_insights, headers={"Authorization": f'Bearer {AUTH_TOKEN}'})

            if response_insights.status_code != 200:
                continue  # Se der erro em um insight, pula para o próximo

            insights = response_insights.json()

            for insight in insights.get("insights", []):
                insight["Platform"] = platform  # Adiciona a plataforma
                insight["Account Name"] = account_name  # Adiciona o nome da conta
                insights_data.append(insight)

        return insights_data
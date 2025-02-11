import requests
from flask import jsonify

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
    def get_plataforms(self, platform):
        "Pega a lista de plataformas disponíveis"

        url = f"{BASE_URL}/platforms"
        response = requests.get(url, headers={"Authorization": f'Bearer {AUTH_TOKEN}'})

        if response.status_code != 200:
            return {"error": "Erro ao buscar dados da plataforma"}, 500
        
        accounts_data = response.json()

        table = []

        for account in accounts_data.get("accounts", []):
            table.append({
                "Platform": platform,
                "Ad Name": account.get("ad_name", ""),
                "followers": account.get("followers"),
                "Clicks": account.get("clicks", 0),
            })

        return response.json()
    
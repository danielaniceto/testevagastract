import requests
from flask import jsonify, Response
import io
import csv
import logging

AUTH_TOKEN = "Bearer ProcessoSeletivoStract2025"
BASE_URL = "https://sidebar.stract.to/api/accounts"

logging.basicConfig(level=logging.INFO)

class ControllerCandidato:
    @staticmethod
    def dados_candidato():
        return {
                "nome": "Daniel Gustavo Aniceto",
                "email": "danielgustavots@gmail.com",
                "linkedin": "https://www.linkedin.com/in/daniel-gustavo-aniceto-63908710b/"
            }
    
class ControllerPlataforma:
    @staticmethod
    def get_plataforma(plataforma):
        url = f"{BASE_URL}/api/accounts?platform={plataforma}"
        response = requests.get(url, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})

        logging.info(f"EU SOU O RESPONSE: {response}")

        if response.status_code != 200:
            return jsonify({"error": "Erro ao buscar dados"}), 500
        
        data = response.json()

        accounts = data.get("accounts", [])

        if not accounts:
            return jsonify({"error": "Nenhum dado foi encontrado"}), 404
        
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["Plataforma", "Nome do Anúncio", "Clicks"])

        for account in accounts:
            writer.writerow([
                plataforma,
                account.get("ad_name", "Sem Nome"),
                account.get("clicks", 0)
            ])

        response = Response(output.getvalue(), content_type="text/csv")
        response.headers["Content-Disposition"] = f"attachment; filename={plataforma}_report.csv"

        return response
    
    @staticmethod
    def get_plataforma_resumo(plataforma):
        url = f"{BASE_URL}/api/accounts?platform={plataforma}"
        response = requests.get(url, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        if response.status_code != 200:
            return jsonify({"error": "Erro ao buscar dados"}), 500
        data = response.json()
        summary = []
        accounts = {}
        for account in data["accounts"]:
            name = account.get("ad_name")
            if name not in accounts:
                accounts[name] = {"Clicks": 0}
            accounts[name]["Clicks"] += account.get("clicks", 0)
        
        for ad_name, stats in accounts.items():
            summary.append({
                "Platform": plataforma,
                "Ad Name": ad_name,
                "Clicks": stats["Clicks"]
            })
        return jsonify(summary)
    
    @staticmethod
    def get_geral():
        url = f"{BASE_URL}/api/platforms"
        response = requests.get(url, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        if response.status_code != 200:
            return jsonify({"error": "Erro ao buscar dados"}), 500
        platforms = response.json()["platforms"]
        all_ads = []
        for platform in platforms:
            all_ads.extend(ControllerPlataforma.get_plataforma(platform))
        return jsonify(all_ads)
    
    @staticmethod
    def get_geral_resumo():
        url = f"{BASE_URL}/api/platforms"
        response = requests.get(url, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        if response.status_code != 200:
            return jsonify({"error": "Erro ao buscar dados"}), 500
        platforms = response.json()["platforms"]
        all_summary = []
        for platform in platforms:
            all_summary.extend(ControllerPlataforma.get_plataforma_resumo(platform))
        return jsonify(all_summary)
    
    @staticmethod
    def get_plataforma_csv(plataforma):
        url = f"{BASE_URL}/api/accounts?platform={plataforma}"
        response = requests.get(url, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        
        if response.status_code != 200:
            return jsonify({"error": "Erro ao buscar dados"}), 500
        
        data = response.json()
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["Platform", "Ad Name", "Clicks"])
        writer.writeheader()

        for account in data["accounts"]:
            writer.writerow({"Platform": plataforma, "Ad Name": account.get("ad_name"), "Clicks": account.get("clicks")})
        output.seek(0)

        return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=platform_report.csv"})
    
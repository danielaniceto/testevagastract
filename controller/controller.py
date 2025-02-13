import requests
from flask import jsonify, Response, send_file
import io
import csv
import logging
from collections import defaultdict

AUTH_TOKEN = "ProcessoSeletivoStract2025"
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
        url = f"{BASE_URL}?plataforma={plataforma}"
        logging.info(f"URL GERADA: {url}")

        response = requests.get(url, headers={"Authorization": AUTH_TOKEN})

        logging.info(f"EU SOU O RESPONSE STATUS: {response.status_code}")
        logging.info(f"EU SOU O RESPONSE JSON: {response.text}")

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
        url = f"{BASE_URL}?plataforma={plataforma}"
    
        response = requests.get(url, headers={"Authorization": AUTH_TOKEN})
    
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Body: {response.text}")
        
        if response.status_code != 200:
            return jsonify({"error": "Erro ao buscar dados"}), 500

        data = response.json()
        
        if 'accounts' not in data:
            return jsonify({"message": "Nenhum dado encontrado para a plataforma"}), 404
        
        resumo = defaultdict(lambda: {"Platform": plataforma, "Ad Name": "", "Clicks": 0})
        
        for account in data["accounts"]:
            nome_conta = account.get("account_name", "Desconhecido")
            
            resumo[nome_conta]["Clicks"] += account.get("clicks", 0)
            
            resumo[nome_conta]["Ad Name"] = ""

        csv_filename = f"{plataforma}_resumo.csv"

        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Platform", "Ad Name", "Clicks"])
            writer.writeheader()
            writer.writerows(resumo.values())

        return send_file(csv_filename, as_attachment=True)
    
    @staticmethod
    def get_geral():
        plataformas = ["facebook", "google", "tiktok", "linkedin"]
        all_ads = []

        for plataforma in plataformas:
            url = f"{BASE_URL}?plataforma={plataforma}"
            response = requests.get(url, headers={"Authorization": AUTH_TOKEN})
            
            logging.info(f"Status Code {plataforma}: {response.status_code}")
            logging.info(f"Response JSON {plataforma}: {response.text}")

            if response.status_code == 200:
                data = response.json()
                if "accounts" in data:
                    for account in data["accounts"]:
                        ad = {
                            "Platform": plataforma,
                            "Account Name": account.get("account_name", ""),
                            "Ad Name": account.get("ad_name", ""),
                            "Clicks": account.get("clicks", ""),
                            "Spend": account.get("spend", ""),
                            "Cost per Click": round(account.get("spend", 0) / account.get("clicks", 1), 2) if plataforma == "google" else account.get("cost_per_click", ""),
                            "Impressions": account.get("impressions", ""),
                            "Conversions": account.get("conversions", ""),
                        }
                        all_ads.append(ad)
        
        if not all_ads:
            return jsonify({"message": "Nenhum dado encontrado para as plataformas"}), 404

        csv_filename = "geral.csv"

        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Platform", "Account Name", "Ad Name", "Clicks", "Spend", "Cost per Click", "Impressions", "Conversions"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_ads)

        return send_file(csv_filename, as_attachment=True)

    @staticmethod
    def get_geral_resumo():
        plataformas = ["facebook", "google", "tiktok", "linkedin"]
        resumo_por_plataforma = {}

        for plataforma in plataformas:
            url = f"{BASE_URL}?plataforma={plataforma}"
            response = requests.get(url, headers={"Authorization": AUTH_TOKEN})

            logging.info(f"Status Code {plataforma}: {response.status_code}")
            logging.info(f"Response JSON {plataforma}: {response.text}")

            if response.status_code == 200:
                data = response.json()
                if "accounts" in data:
                    for account in data["accounts"]:
                        if plataforma not in resumo_por_plataforma:
                            resumo_por_plataforma[plataforma] = {
                                "Platform": plataforma,
                                "Clicks": 0,
                                "Spend": 0,
                                "Cost per Click": 0,
                                "Impressions": 0,
                                "Conversions": 0
                            }

                        resumo_por_plataforma[plataforma]["Clicks"] += account.get("clicks", 0)
                        resumo_por_plataforma[plataforma]["Spend"] += account.get("spend", 0)
                        resumo_por_plataforma[plataforma]["Impressions"] += account.get("impressions", 0)
                        resumo_por_plataforma[plataforma]["Conversions"] += account.get("conversions", 0)

                    clicks_total = resumo_por_plataforma[plataforma]["Clicks"]
                    spend_total = resumo_por_plataforma[plataforma]["Spend"]
                    resumo_por_plataforma[plataforma]["Cost per Click"] = round(spend_total / clicks_total, 2) if clicks_total > 0 else 0

        if not resumo_por_plataforma:
            return jsonify({"message": "Nenhum dado encontrado para as plataformas"}), 404

        csv_filename = "geral_resumo.csv"

        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Platform", "Clicks", "Spend", "Cost per Click", "Impressions", "Conversions"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(resumo_por_plataforma.values())

        return send_file(csv_filename, as_attachment=True)

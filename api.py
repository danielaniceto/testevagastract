from flask import jsonify
import requests
import io
import csv
from controller import ControllerCandidato, ControllerPlataforma

def api_routes(app):
    @app.route('/')
    def candidato():
        return jsonify(ControllerCandidato.dados_candidato())
           
    @app.route('/<platforms>')
    def plataform_report():
        return jsonify(ControllerPlataforma.get_plataforms)

    
    @app.route('/<platform>/csv')
    def platform_report_csv(platform):
        # Requisição à API externa para pegar os dados
        url = f"https://sidebar.stract.to/api/accounts?platform={platform}"
        response = requests.get(url, headers={'Authorization': 'Bearer ProcessoSeletivoStract2025'})
        
        if response.status_code != 200:
            return jsonify({"error": "Erro ao buscar dados da plataforma"}), 500

        accounts_data = response.json()

        # Criação do CSV
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["Platform", "Ad Name", "Clicks"])
        writer.writeheader()
        
        for account in accounts_data.get('accounts', []):
            writer.writerow({
                "Platform": platform,
                "Ad Name": account.get('ad_name', ''),
                "Clicks": account.get('clicks', 0)
            })

        # Retorna o CSV como resposta HTTP
        output.seek(0)
        return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=platform_report.csv"})

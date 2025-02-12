from flask import jsonify, Flask
from controller.controller import ControllerCandidato, ControllerPlataforma

app = Flask(__name__)

def api_routes(app):
    @app.route('/')
    def candidato():
        return jsonify(ControllerCandidato.dados_candidato())
           
    @app.route('/<platform>')
    def get_plataform_report(platform):
        insights = ControllerPlataforma.get_insights_by_platform(platform)
        return jsonify(insights)
    
    @app.route('/<platform>/resumo')
    def platform_sumary(platform):
        insights = ControllerPlataforma.get_insights_by_platform(platform)
        return jsonify({"total": len(insights)})

if __name__ == '__main__':
    app.run(debug=True)
  
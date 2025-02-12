from flask import jsonify, Flask
from controller.controller import ControllerCandidato, ControllerPlataforma

app = Flask(__name__)

def api_routes(app):
    @app.route('/')
    def candidato():
        return jsonify(ControllerCandidato.dados_candidato())
           
    @app.route('/<plataforma>')
    def get_plataform_report(platform):
        return ControllerPlataforma.get_plataforma(platform)
    
    @app.route('/<platform>/resumo')
    def platforma_resumo(platform):
        return ControllerPlataforma.get_plataforma_resumo(platform)
    
    @app.route('/geral')
    def geral():
        return ControllerPlataforma.get_geral()
    
    @app.route('/geral/resumo')
    def geral_resumo():
        return ControllerPlataforma.get_geral_resumo()

if __name__ == '__main__':
    app.run(debug=True)
  
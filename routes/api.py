from flask import jsonify, Flask
from controller.controller import ControllerCandidato, ControllerPlataforma

app = Flask(__name__)

def api_routes(app):
    @app.route('/')
    def candidato():
        return jsonify(ControllerCandidato.dados_candidato())
           
    @app.route("/<string:plataforma>")
    def get_plataforma(plataforma):
        return ControllerPlataforma.get_plataforma(plataforma)
    
    @app.route("/<string:plataforma>/resumo")
    def platforma_resumo(plataforma):
        return ControllerPlataforma.get_plataforma_resumo(plataforma)
    
    @app.route("/geral")
    def geral():
        return ControllerPlataforma.get_geral()
    
    @app.route("/geral/resumo")
    def geral_resumo():
        return ControllerPlataforma.get_geral_resumo()

if __name__ == '__main__':
    app.run(debug=True)
  
from flask import Flask
from testevagastract.routes.api import api_routes

app = Flask(__name__)

api_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
    
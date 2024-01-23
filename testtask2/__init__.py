from flask import Flask
from testtask2.map_page import map_page


def create_app():
    app = Flask(__name__)
    key = '12345'
    app.secret_key = key
    app.register_blueprint(map_page)

    return app

from flask import Flask, Response, make_response
import logging

logging.basicConfig(level=logging.INFO)

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index() -> Response:
        return make_response({'message': "Api"}, 200)

    return app

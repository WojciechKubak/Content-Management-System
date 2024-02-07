from gateway.config import services
from flask import Flask, Response, make_response, request
import logging
import httpx

logging.basicConfig(level=logging.INFO)


def create_app() -> Response:
    app = Flask(__name__)

    with app.app_context():
        
        @app.route('/api/<service>/<path:path>')
        def gateway(service: str, path: str) -> Response:
            
            if service not in services:
                return make_response({'message': 'Invalid service'}, 400)

            response = httpx.request(
                method=request.method,
                url=f"{services[service]['url']}/{path}",
                headers=request.headers,
                data=request.get_data(),
                params=request.args
            )

            return (response.content, response.status_code, response.headers.items())

        return app

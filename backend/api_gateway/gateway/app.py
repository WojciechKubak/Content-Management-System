from gateway.config import services, redis_config
from flask import Flask, Response, make_response, request
from flask_caching import Cache
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import httpx

logging.basicConfig(level=logging.INFO)


def create_app() -> Response:
    app = Flask(__name__)
    app.config |= redis_config

    cache = Cache(app)

    with app.app_context():

        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=0
        )
        
        @app.route('/api/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        @cache.cached(timeout=50, key_prefix=lambda: request.path + request.method)
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

            return (response.content, response.status_code, dict(response.headers.items()))

        return app

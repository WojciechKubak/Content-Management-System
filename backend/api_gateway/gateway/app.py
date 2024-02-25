from gateway.security.configure_security import configure_security
from gateway.config import redis_config, security_config
from gateway.route.user import user_blueprint
from gateway.route.article import article_blueprint
from flask import Flask, Response, make_response


def create_app() -> Flask:
    app = Flask(__name__)

    app.config |= security_config
    app.config |= redis_config

    from gateway.extensions import jwt_manager, cache
    jwt_manager.init_app(app)
    cache.init_app(app)

    configure_security(app)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(article_blueprint)

    with app.app_context():
        
        @app.get('/')
        def index() -> Response:
            return make_response({'message': 'Gateway service is running'}, 200)

        return app

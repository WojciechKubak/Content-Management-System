from gateway.config import Config
from gateway.security.configure_security import configure_security
from gateway.extensions import jwt_manager, cache
from gateway.route.user import user_blueprint
from gateway.route.article import article_blueprint
from flask import Flask, Response, make_response


def create_app(config: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

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

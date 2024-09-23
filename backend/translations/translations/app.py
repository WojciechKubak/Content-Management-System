from translations.exception_handler import error_handler_register
from translations.api.background_tasks import register_start_pooling
from translations.config.environments import production
from translations.db.configuration import sa
from translations.api.translations import translations_bp
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, Response, make_response
from flask_migrate import Migrate
from flask_executor import Executor
import logging


logging.basicConfig(level=logging.INFO)


def create_app(config: object = production) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config)

    executor = Executor(app)
    register_start_pooling(app, executor)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    error_handler_register(app)

    app.register_blueprint(translations_bp)

    sa.init_app(app)
    _ = Migrate(app, sa)

    with app.app_context():

        @app.route("/health")
        def health() -> Response:
            return make_response({"message": "OK"}, 200)

        return app

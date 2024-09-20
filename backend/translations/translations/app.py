from translations.api.background_tasks import background_tasks_register
from translations.api.exception_handler import error_handler_register
from translations.db.configuration import sa
from translations.api.translations import translations_bp
from translations.config.config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, Response, make_response
from flask_executor import Executor
from flask_migrate import Migrate
import logging


logging.basicConfig(level=logging.INFO)


def create_app(config: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    error_handler_register(app)

    app.register_blueprint(translations_bp)

    sa.init_app(app)
    _ = Migrate(app, sa)

    executor = Executor(app)
    background_tasks_register(app, executor)

    with app.app_context():

        @app.route("/health")
        def health() -> Response:
            return make_response({"message": "OK"}, 200)

        return app

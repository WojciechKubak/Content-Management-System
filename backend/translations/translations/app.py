from translations.broker.setup import setup_start_pooling
from translations.persistance.configuration import sa
from translations.api.routes import translations_bp
from translations.config import Config
from flask import Flask, Response, make_response
from flask_executor import Executor
from flask_migrate import Migrate
import logging

logging.basicConfig(level=logging.INFO)


def create_app(config: Config) -> Flask:
    """
    Create a Flask application.

    Args:
        config (Config): The configuration object to use.

    Returns:
        Flask: The created Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(translations_bp)

    sa.init_app(app)
    migrate = Migrate(app, sa)

    executor = Executor(app)
    setup_start_pooling(app, executor)

    with app.app_context():

        @app.route('/health')
        def health() -> Response:
            """
            Health check route.

            Returns:
                Response: A Flask Response object with a JSON containing a health check message.
            """
            return make_response({'message': 'OK'}, 200)

        return app

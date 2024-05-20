from users.email.configuration import mail
from users.persistance.configuration import sa
from users.config import Config
from flask import Flask, Response, make_response
from flask_migrate import Migrate
import logging


logging.basicConfig(level=logging.INFO)

def create_app(config: Config) -> Flask:
    """
    Creates and configures the Flask application.

    Args:
        config (Config): The configuration object to use.

    Returns:
        Flask: The configured Flask application.
    """
    
    app = Flask(__name__)
    app.config.from_object(config)
    
    sa.init_app(app)
    migrate = Migrate(app, sa)
    mail.init_app(app)

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

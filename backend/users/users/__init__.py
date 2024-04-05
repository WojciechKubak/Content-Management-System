from users.extensions import sa, mail_config
from users.config import Config
from users.routes.user import (
    UserIdResource,
    UserNameResource,
    UserListResource,
    UserRegisterResource,
    UserActivationResource,
    UserCredentalsResource
)
from users.routes.comment import (
    CommentIdResource,
    CommentResource,
    CommentContentResource,
    CommentUserIdResource,
    CommentArticleIdResource,
)
from flask import Flask, Response, make_response
from flask_restful import Api



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
    mail_config.init_app(app)

    api = Api(app, prefix='/users')
    api.add_resource(UserIdResource, '/<int:id_>')
    api.add_resource(UserNameResource, '/<string:username>')
    api.add_resource(UserListResource, '/')
    api.add_resource(UserActivationResource, '/activate')
    api.add_resource(UserRegisterResource, '/register')
    api.add_resource(UserCredentalsResource, '/credentials')

    api.add_resource(CommentIdResource, '/comments/<int:id_>')
    api.add_resource(CommentResource, '/comments')
    api.add_resource(CommentContentResource, '/comments/<int:id_>')
    api.add_resource(CommentUserIdResource, '/comments/user/<int:id_>')
    api.add_resource(CommentArticleIdResource, '/comments/article/<int:id_>')

    with app.app_context():

        @app.route('/health')
        def index() -> Response:
            """Default route fot health check"""
            return make_response({'message': f'Users home page'}, 200)

        return app

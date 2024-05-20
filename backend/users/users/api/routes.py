from users.api.configuration import user_service, comment_service
from flask import Blueprint, Response, make_response, request


user_bp = Blueprint('users', __name__, url_prefix='/users')
comment_bp = Blueprint('comments', __name__, url_prefix='/comments')
user_bp.register_blueprint(comment_bp)

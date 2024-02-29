from gateway.security.role_auth import requires_roles, requires_no_jwt
from gateway.service.configuration import user_service
from gateway.extensions import cache
from flask import Blueprint, Response, make_response, request
from typing import Any

user_blueprint = Blueprint('users', __name__, url_prefix='/api/users')


def handle_user_request(method: str, endpoint: str, data: dict[str, Any] | None = None) -> Response:
    """
    Handles a user request.

    Args:
        method (str): The HTTP method of the request.
        endpoint (str): The endpoint of the request.
        data (dict[str, Any] | None): The data of the request.

    Returns:
        Response: The response of the request.
    """
    try:
        response_data, status_code = user_service.process_request(method, endpoint, data)
        return make_response(response_data, status_code)
    except ConnectionError as e:
        return make_response({'message': str(e)}, 500)


@user_blueprint.route('/health', methods=['GET'])
@requires_roles(['admin'])
def health_check() -> Response:
    """
    Checks the health of the user service.

    Returns:
        Response: The response of the request.
    """
    try:
        user_service.check_health()
        return make_response({'message': 'Users service is working'}, 200)
    except ConnectionError as e:
         return make_response({'message': str(e)}, 500)


@user_blueprint.route('/comments/<int:comment_id>', methods=['GET'])
@cache.cached(timeout=50)
def get_comment(comment_id: int) -> Response:
    """Gets a specific comment by its ID."""
    return handle_user_request(request.method, f'users/comments/{comment_id}')


@user_blueprint.route('/comments', methods=['POST'])
@requires_roles(['admin', 'user', 'redactor', 'translator'])
def post_comment() -> Response:
    """Posts a new comment."""
    return handle_user_request(request.method, f'users/comments', request.json)


@user_blueprint.route('/comments/<int:comment_id>', methods=['PUT'])
@requires_roles(['admin'])
def put_comment(comment_id: int) -> Response:
    """Updates a comment."""
    return handle_user_request(request.method, f'users/comments/{comment_id}', request.json)


@user_blueprint.route('/comments/<int:comment_id>', methods=['DELETE'])
@requires_roles(['admin'])
def delete_comment(comment_id: int) -> Response:
    """Deletes a comment."""
    return handle_user_request(request.method, f'users/comments/{comment_id}')


@user_blueprint.route('/<int:user_id>', methods=['GET'])
@cache.cached(timeout=50)
def get_user(user_id: int) -> Response:
    """Gets a specific user by their ID."""
    return handle_user_request(request.method, f'users/{user_id}')


@user_blueprint.route('/', methods=['GET'])
@cache.cached(timeout=50)
def get_users() -> Response:
    """Gets all users."""
    return handle_user_request(request.method, f'users/')


@user_blueprint.route('/<int:user_id>', methods=['PUT'])
@requires_roles(['admin'])
def modify_user(user_id: int) -> Response:
    """Modifies a user."""
    return handle_user_request((request.method, f'users/{user_id}'), request.json)


@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
@requires_roles(['admin'])
def delete_user(user_id: int) -> Response:
    """Deletes a user."""
    return handle_user_request((request.method, f'users/{user_id}'))


@user_blueprint.route('/register', methods=['POST'])
@requires_no_jwt()
def user_register() -> Response:
    """Registers a new user."""
    return handle_user_request(request.method, 'users/register', request.json)

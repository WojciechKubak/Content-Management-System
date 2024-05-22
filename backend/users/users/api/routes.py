from users.api.exceptions import (
    UserNotFoundException, 
    CommentNotFoundException,
    UserNameInUseException,
    EmailInUseException,
    UserNotFoundException,
    UserAlreadyActiveException,
    IncorrectPasswordException,
    UserNotActiveException,
    InvalidRoleException,
    ActivationLinkExpiredException,
    NotCommentOwnerException
)
from users.api.configuration import user_service, comment_service
from flask import Blueprint, Response, make_response, request


user_bp = Blueprint('users', __name__, url_prefix='/users')
comment_bp = Blueprint('comments', __name__, url_prefix='/comments')
user_bp.register_blueprint(comment_bp)


@user_bp.put('/<int:id_>/role')
def update_user_role(id_: int) -> Response:
    """
    Updates the role of a user.

    Args:
        id_ (int): User ID.

    Returns:
        Response: Flask Response object with updated user data or error message.
    """
    role = request.json.get('role')
    try:
        user = user_service.change_user_role(id_, role)
        return make_response(user.to_dict(), 200)
    except (UserNotFoundException, InvalidRoleException) as e:
        return make_response({'message': str(e)}, 400)


@user_bp.put('/<int:id_>/username')
def update_user_username(id_: int) -> Response:
    """
    Updates the username of a user.

    Args:
        id_ (int): User ID.

    Returns:
        Response: Flask Response object with updated user data or error message.
    """
    username = request.json.get('username')
    try:
        user = user_service.change_user_username(id_, username)
        return make_response(user.to_dict(), 200)
    except (UserNotFoundException, UserNameInUseException) as e:
        return make_response({'message': str(e)}, 400)


@user_bp.delete('/<int:id_>')
def delete_user(id_: int) -> Response:
    """
    Deletes a user.

    Args:
        id_ (int): User ID.

    Returns:
        Response: Flask Response object with deleted user's ID or error message.
    """
    try:
        user_id = user_service.delete_user(id_)
        return make_response({'id': user_id}, 200)
    except UserNotFoundException as e:
        return make_response({'message': str(e)}, 400)


@user_bp.get('/username/<string:username>')
def get_user_by_username(username: str) -> Response:
    """
    Retrieves a user by username.

    Args:
        username (str): Username of the user.

    Returns:
        Response: Flask Response object with user data or error message.
    """
    try:
        user = user_service.get_user_by_username(username)
        return make_response(user.to_dict(), 200)
    except UserNotFoundException as e:
        return make_response({'message': str(e)}, 400)


@user_bp.get('/email/<string:email>')
def get_user_by_email(email: str) -> Response:
    """
    Retrieves a user by email.

    Args:
        email (str): Email of the user.

    Returns:
        Response: Flask Response object with user data or error message.
    """
    try:
        user = user_service.get_user_by_email(email)
        return make_response(user.to_dict(), 200)
    except UserNotFoundException as e:
        return make_response({'message': str(e)}, 400)


@user_bp.get('/<int:id_>')
def get_user_by_id(id_: int) -> Response:
    """
    Retrieves a user by ID.

    Args:
        id_ (int): ID of the user.

    Returns:
        Response: Flask Response object with user data or error message.
    """
    try:
        user = user_service.get_user_by_id(id_)
        return make_response(user.to_dict(), 200)
    except UserNotFoundException as e:
        return make_response({'message': str(e)}, 400)


@user_bp.get('/', strict_slashes=False)
def get_all_users() -> Response:
    """
    Retrieves all users.

    Returns:
        Response: Flask Response object with a list of all user data.
    """
    users = user_service.get_all_users()
    return make_response([user.to_dict() for user in users], 200)


@user_bp.get('/activate')
def activate_user() -> Response:
    """
    Activates a user.

    Args:
        user_id (int): ID of the user.
        timestamp (float): Timestamp of the activation request.

    Returns:
        Response: Flask Response object with user data or error message.
    """
    user_id = int(request.args.get('id'))
    timestamp = float(request.args.get('timestamp'))
    try:
        user = user_service.activate_user(user_id, timestamp)
        return make_response(user.to_dict(), 200)
    except (ActivationLinkExpiredException, UserNotFoundException, UserAlreadyActiveException) as e:
        return make_response({'message': str(e)}, 400)


@user_bp.post('/credentials')
def verify_credentials() -> Response:
    """
    Verifies user credentials.

    Args:
        username (str): Username of the user.
        password (str): Password of the user.

    Returns:
        Response: Flask Response object with user data or error message.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    try:
        user = user_service.verify_credentials(username, password)
        return make_response(user.to_dict(), 200)
    except (UserNotFoundException, IncorrectPasswordException, UserNotActiveException) as e:
        return make_response({'message': str(e)}, 400)


@user_bp.post('/register')
def register_user() -> Response:
    """
    Registers a new user.

    Returns:
        Response: Flask Response object with user data or error message.
    """
    data = request.get_json()
    try:
        user = user_service.register_user(data)
        return make_response(user.to_dict(), 200)
    except (UserNameInUseException, EmailInUseException) as e:
        return make_response({'message': str(e)}, 400)


@comment_bp.post('/', strict_slashes=False)
def add_comment() -> Response:
    """
    Adds a new comment.

    Returns:
        Response: Flask Response object with comment data or error message.
    """
    data = request.get_json()
    try:
        comment = comment_service.add_comment(data)
        return make_response(comment.to_dict(), 201)
    except UserNotFoundException as e:
        return make_response({'message': str(e)}, 400)


@comment_bp.put('/<int:id_>')
def update_comment_content(id_: int) -> Response:
    """
    Updates the content of a comment.

    Args:
        id_ (int): ID of the comment.

    Returns:
        Response: Flask Response object with updated comment data or error message.
    """
    data = request.get_json()
    try:
        comment = comment_service.update_comment_content({'id_': id_} | data)
        return make_response(comment.to_dict(), 200)
    except (CommentNotFoundException, NotCommentOwnerException) as e:
        return make_response({'message': str(e)}, 400)


@comment_bp.delete('/<int:id_>')
def delete_comment(id_: int) -> Response:
    """
    Deletes a comment.

    Args:
        id_ (int): ID of the comment.

    Returns:
        Response: Flask Response object with deleted comment's ID or error message.
    """
    try:
        comment_id = comment_service.delete_comment(id_)
        return make_response({'id': comment_id}, 200)
    except CommentNotFoundException as e:
        return make_response({'message': str(e)}, 400)
    

@comment_bp.get('/<int:id_>')
def get_comment_by_id(id_: int) -> Response:
    """
    Retrieves a comment by ID.

    Args:
        id_ (int): ID of the comment.

    Returns:
        Response: Flask Response object with comment data or error message.
    """
    try:
        comment = comment_service.get_comment_by_id(id_)
        return make_response(comment.to_dict(), 200)
    except CommentNotFoundException as e:
        return make_response({'message': str(e)}, 400)
    

@comment_bp.get('/user/<int:id_>')
def get_user_comments(id_: int) -> Response:
    """
    Retrieves all comments of a user.

    Args:
        id_ (int): ID of the user.

    Returns:
        Response: Flask Response object with a list of user's comment data.
    """
    comments = comment_service.get_user_comments(id_)
    return make_response([comment.to_dict() for comment in comments], 200)


@comment_bp.get('article/<int:id_>')
def get_article_comments(id_: int) -> Response:
    """
    Retrieves all comments of an article.

    Args:
        id_ (int): ID of the article.

    Returns:
        Response: Flask Response object with a list of article's comment data.
    """
    comments = comment_service.get_article_comments(id_)
    return make_response([comment.to_dict() for comment in comments], 200)

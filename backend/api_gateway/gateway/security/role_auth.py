from gateway.service.configuration import auth_service
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from flask import Response, make_response
from typing import Callable, Any
from functools import wraps


def requires_roles(roles: list[str]) -> Callable:
    """
    Decorator that checks if the user has one of the required roles.

    Args:
        roles (list[str]): The roles to check.

    Returns:
        Callable: The decorated function.
    """

    def decorator(fn: Callable) -> Callable:
        """
        The decorated function.

        Returns:
            Response: The response of the request.
        """
        @wraps(fn)
        def decorated(*args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
            try:
                _, jwt_data = verify_jwt_in_request()
                user = auth_service.identify_user(jwt_data.get('sub'))
                if user.get('role', '').lower() in [role.lower() for role in roles]:
                    return fn(*args, **kwargs)
                else:
                    return make_response({'message': 'Insufficient permissions'}, 403)
            except (NoAuthorizationError, InvalidHeaderError):
                return make_response({'message': 'Token is missing or invalid'}, 401)
        return decorated
    return decorator


def requires_no_jwt() -> Callable:
    """
    Decorator that checks if the user is not authenticated.

    Returns:
        Callable: The decorated function.
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def decorated(*args, **kwargs):
            """
            The decorated function.

            Returns:
                Response: The response of the request.
            """
            try:
                verify_jwt_in_request()
                return make_response({'message': 'You are already authenticated'}, 403)
            except:
                return fn(*args, **kwargs)
        return decorated
    return decorator

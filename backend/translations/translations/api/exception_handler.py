from translations.core.exceptions import (
    ConfigurationError,
    ApplicationError,
    ValidationError,
)
from flask import Flask, Response, make_response


def register_error_handler(app: Flask) -> None:

    @app.errorhandler(Exception)
    def custom_exception_handler(exception: Exception) -> Response:
        if isinstance(exception, (ConfigurationError, ValidationError)):
            return make_response({"message": exception.message}, 400)

        if isinstance(exception, ApplicationError):
            return make_response({"message": exception.message}, 500)

        return make_response({"message": "An unexpected error occurred"}, 500)

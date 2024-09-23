from translations.core.exceptions import (
    ConfigurationError,
    ApplicationError,
    ValidationError,
    StorageError,
    TranslationError,
)
from flask import Flask, Response, make_response


def error_handler_register(app: Flask) -> None:

    @app.errorhandler(Exception)
    def custom_exception_handler(exception: Exception) -> Response:
        if isinstance(exception, (ConfigurationError, ValidationError)):
            return make_response({"message": exception.message}, 400)

        if isinstance(exception, (StorageError, TranslationError)):
            return make_response({"message": exception.message}, 500)

        if isinstance(exception, ApplicationError):
            return make_response({"message": "An internal server error occurred"}, 500)

        return make_response({"message": "An unexpected error occurred"}, 500)

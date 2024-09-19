from translations.gpt.exceptions import ChatGptServiceError
from translations.api.configuration import api_service
from flask import Blueprint, Response, make_response, request
from translations.api.exceptions import (
    EntityNotFoundError,
    TranslationNotPendingError,
    MissingDataError,
    InvalidRedactorIdError,
    InvalidStatusOperationError,
    TranslationAlreadyReleasedError,
)

translations_bp = Blueprint("translations", __name__, url_prefix="/translations")


@translations_bp.get("/")
def get_all_translations() -> Response:
    """
    Get all translations.

    Returns:
        Response: A Flask Response object with a JSON containing all translations.
    """
    translations = api_service.get_all_translations()
    return make_response(
        {"translations": [translation.to_dict() for translation in translations]}, 200
    )


@translations_bp.get("/<int:translation_id>")
def get_translation_by_id(translation_id: int) -> Response:
    """
    Get a translation by its ID.

    Args:
        translation_id (int): The ID of the translation.

    Returns:
        Response: A Flask Response object with a JSON containing the translation or an error message.
    """
    try:
        translation = api_service.get_translation_by_id(translation_id)
        return make_response(translation.to_dict(), 200)
    except EntityNotFoundError as e:
        return make_response({"message": str(e)}, 400)


@translations_bp.get("/language/<int:language_id>")
def get_translations_by_language(language_id: int) -> Response:
    """
    Get translations by language ID.

    Args:
        language_id (int): The ID of the language.

    Returns:
        Response: A Flask Response object with a JSON containing the translations or an error message.
    """
    try:
        translations = api_service.get_translations_by_language(language_id)
        return make_response(
            {"translations": [translation.to_dict() for translation in translations]},
            200,
        )
    except EntityNotFoundError as e:
        return make_response({"message": str(e)}, 400)


@translations_bp.put("/<int:translation_id>/content")
def update_translation_content(translation_id: int) -> Response:
    """
    Update a translation's content.

    Args:
        translation_id (int): The ID of the translation.

    Returns:
        Response: A Flask Response object with a JSON containing the updated translation or an error message.
    """
    try:
        new_content = request.json.get("content")
        updated_translation = api_service.change_translation_content(
            translation_id, new_content
        )
        return make_response(updated_translation.to_dict(), 200)
    except (EntityNotFoundError, TranslationNotPendingError, MissingDataError) as e:
        return make_response({"message": str(e)}, 400)


@translations_bp.put("/<int:translation_id>/title")
def update_translation_title(translation_id: int) -> Response:
    """
    Update a translation's title.

    Args:
        translation_id (int): The ID of the translation.

    Returns:
        Response: A Flask Response object with a JSON containing the updated translation or an error message.
    """
    try:
        new_title = request.json.get("title")
        updated_translation = api_service.change_translation_title(
            translation_id, new_title
        )
        return make_response(updated_translation.to_dict(), 200)
    except (EntityNotFoundError, TranslationNotPendingError, MissingDataError) as e:
        return make_response({"message": str(e)}, 400)


@translations_bp.put("/<int:translation_id>/status")
def update_translation_status(translation_id: int) -> Response:
    """
    Update a translation's status.

    Args:
        translation_id (int): The ID of the translation.

    Returns:
        Response: A Flask Response object with a JSON containing the updated translation or an error message.
    """
    try:
        status = request.json.get("status")
        redactor_id = request.json.get("redactor_id")
        updated_translation = api_service.change_translation_status(
            translation_id, status, redactor_id
        )
        return make_response(updated_translation.to_dict(), 200)
    except (
        EntityNotFoundError,
        InvalidRedactorIdError,
        InvalidStatusOperationError,
        TranslationAlreadyReleasedError,
    ) as e:
        return make_response({"message": str(e)}, 400)


@translations_bp.post("/<int:translation_id>/translate/title")
def generate_title_translation(translation_id: int) -> Response:
    """
    Generate a translation for a title.

    Args:
        translation_id (int): The ID of the translation.

    Returns:
        Response: A Flask Response object with a JSON containing the translated title or an error message.
    """
    try:
        result = api_service.translate_title(translation_id)
        return make_response({"title": result}, 200)
    except (EntityNotFoundError, TranslationNotPendingError, ChatGptServiceError) as e:
        return make_response({"message": str(e)}, 400)


@translations_bp.post("/<int:translation_id>/translate/content")
def generate_content_translation(translation_id: int) -> Response:
    """
    Generate a translation for content.

    Args:
        translation_id (int): The ID of the translation.

    Returns:
        Response: A Flask Response object with a JSON containing the translated content or an error message.
    """
    try:
        result = api_service.translate_content(translation_id)
        return make_response({"content": result}, 200)
    except (EntityNotFoundError, TranslationNotPendingError, ChatGptServiceError) as e:
        return make_response({"message": str(e)}, 400)

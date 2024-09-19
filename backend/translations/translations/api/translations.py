from translations.services.translations import (
    get_translation_by_id,
    get_translations_by_language,
    get_all_translations,
    change_translation_content,
    change_translation_title,
    change_translation_status,
    translate_title,
    translate_content,
)
from flask import Blueprint, Response, make_response, request


translations_bp = Blueprint("translations", __name__, url_prefix="/translations")


@translations_bp.get("/")
def translation_list() -> Response:
    translations = get_all_translations()
    return make_response(
        {"translations": [translation.to_dict() for translation in translations]}, 200
    )


@translations_bp.get("/<int:translation_id>")
def translation_detail_api_by_id(translation_id: int) -> Response:
    translation = get_translation_by_id(translation_id=translation_id)
    return make_response(translation.to_dict(), 200)


@translations_bp.get("/language/<int:language_id>")
def translation_detail_api_by_language(language_id: int) -> Response:
    translations = get_translations_by_language(language_id=language_id)
    return make_response(
        {"translations": [translation.to_dict() for translation in translations]},
        200,
    )


@translations_bp.put("/<int:translation_id>/content")
def translation_update_content(translation_id: int) -> Response:
    new_content = request.json.get("content")
    updated_translation = change_translation_content(
        translation_id=translation_id, new_content=new_content
    )
    return make_response(updated_translation.to_dict(), 200)


@translations_bp.put("/<int:translation_id>/title")
def translation_update_title(translation_id: int) -> Response:
    new_title = request.json.get("title")
    updated_translation = change_translation_title(
        translation_id=translation_id, new_title=new_title
    )
    return make_response(updated_translation.to_dict(), 200)


@translations_bp.put("/<int:translation_id>/status")
def translation_update_status(translation_id: int) -> Response:
    status = request.json.get("status")
    redactor_id = request.json.get("redactor_id")
    updated_translation = change_translation_status(
        translation_id=translation_id, status_type=status, redactor_id=redactor_id
    )
    return make_response(updated_translation.to_dict(), 200)


@translations_bp.post("/<int:translation_id>/translate/title")
def title_generate_translation(translation_id: int) -> Response:
    result = translate_title(translation_id=translation_id)
    return make_response({"title": result}, 200)


@translations_bp.post("/<int:translation_id>/translate/content")
def content_generate_translation(translation_id: int) -> Response:
    result = translate_content(translation_id=translation_id)
    return make_response({"content": result}, 200)

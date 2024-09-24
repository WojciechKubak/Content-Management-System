from tests.factories import TranslationFactory, Translation
from translations.services.translations import (
    TRANSLATION_NOT_FOUND_ERROR_MSG,
    TRANSLATION_NOT_PENDING_ERROR_MSG,
)
from flask import url_for


def test_api_response_on_failed_due_to_missing_translation(client) -> None:
    url = url_for("translations.content_generate_translation", translation_id=999)

    response = client.post(url)

    assert 400 == response.status_code
    assert TRANSLATION_NOT_FOUND_ERROR_MSG.encode() in response.data


def test_api_response_on_failed_due_to_not_pending_status_of_translation(
    client,
) -> None:
    translation = TranslationFactory(status=Translation.StatusType.COMPLETED)
    url = url_for(
        "translations.content_generate_translation", translation_id=translation.id
    )

    response = client.post(url)

    assert 400 == response.status_code
    assert TRANSLATION_NOT_PENDING_ERROR_MSG.encode() in response.data


def test_api_response_on_success_returns_translated_content(client) -> None:
    translation = TranslationFactory(status=Translation.StatusType.PENDING)
    url = url_for(
        "translations.content_generate_translation", translation_id=translation.id
    )

    response = client.post(url)

    assert 200 == response.status_code
    assert b"TRANSLATED" in response.data

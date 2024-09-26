from tests.factories import TranslationFactory
from translations.services.translations import TRANSLATION_NOT_FOUND_ERROR_MSG
from flask import url_for


def test_api_response_on_failed_due_to_missing_translation(client) -> None:
    url = url_for("translations.translation_detail_api_by_id", translation_id=999)

    response = client.get(url)

    assert 400 == response.status_code
    assert TRANSLATION_NOT_FOUND_ERROR_MSG.encode() in response.data


def test_api_response_on_success_returns_translation_with_read_content(client) -> None:
    translation = TranslationFactory()
    url = url_for(
        "translations.translation_detail_api_by_id", translation_id=translation.id
    )

    response = client.get(url)

    assert 200 == response.status_code
    assert b"CONTENT OF" in response.data

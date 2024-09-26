from tests.factories import TranslationFactory, Translation
from translations.services.translations import (
    TRANSLATION_NOT_FOUND_ERROR_MSG,
    TRANSLATION_NOT_PENDING_ERROR_MSG,
)
from flask import url_for


def test_api_response_on_failed_due_to_missing_translation(client) -> None:
    url = url_for("translations.translation_update_title", translation_id=999)

    response = client.put(url, json={"title": "new_title"})

    assert 400 == response.status_code
    assert TRANSLATION_NOT_FOUND_ERROR_MSG.encode() in response.data


def test_api_response_on_failed_due_to_not_pending_translation_status(client) -> None:
    translation = TranslationFactory(status=Translation.StatusType.COMPLETED)
    url = url_for(
        "translations.translation_update_title", translation_id=translation.id
    )

    response = client.put(url, json={"title": "new_title"})

    assert 400 == response.status_code
    assert TRANSLATION_NOT_PENDING_ERROR_MSG.encode() in response.data


def test_api_response_on_success_returns_translation_with_updated_title(
    client,
) -> None:
    translation = TranslationFactory(status=Translation.StatusType.PENDING)
    url = url_for(
        "translations.translation_update_title", translation_id=translation.id
    )

    response = client.put(url, json={"title": "new_title"})

    assert 200 == response.status_code
    assert "new_title" in response.get_json()["translation_title"]

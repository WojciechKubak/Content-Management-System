from tests.factories import TranslationFactory, Translation
from translations.services.translations import (
    TRANSLATION_NOT_FOUND_ERROR_MSG,
    TRANSLATION_ALREADY_RELEASED_ERROR_MSG,
)
from flask import url_for


def test_api_response_on_failed_due_to_missing_translation(client) -> None:
    url = url_for("translations.translation_update_status", translation_id=999)

    response = client.put(url, json={"status": "completed"})

    assert 400 == response.status_code
    assert TRANSLATION_NOT_FOUND_ERROR_MSG.encode() in response.data


def test_api_response_on_failed_due_to_already_released_translation_status(
    client,
) -> None:
    translation = TranslationFactory(status=Translation.StatusType.RELEASED)
    url = url_for(
        "translations.translation_update_status", translation_id=translation.id
    )

    response = client.put(url, json={"status": "completed"})

    assert 400 == response.status_code
    assert TRANSLATION_ALREADY_RELEASED_ERROR_MSG.encode() in response.data


def test_api_response_on_success_returns_translation_list_dto_with_updated_status(
    client,
) -> None:
    translation = TranslationFactory(status=Translation.StatusType.REQUESTED)
    url = url_for(
        "translations.translation_update_status", translation_id=translation.id
    )

    response = client.put(url, json={"status": "completed"})

    assert 200 == response.status_code
    assert Translation.StatusType.COMPLETED.value == response.get_json()["status"]

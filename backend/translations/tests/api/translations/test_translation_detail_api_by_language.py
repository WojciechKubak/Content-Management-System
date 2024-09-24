from tests.factories import TranslationFactory, LanguageFactory
from translations.services.translations import LANGUAGE_NOT_FOUND_ERROR_MSG
from flask import url_for


def test_api_response_on_failed_due_to_missing_language(client) -> None:
    url = url_for("translations.translation_detail_api_by_language", language_id=999)

    response = client.get(url)

    assert 400 == response.status_code
    assert LANGUAGE_NOT_FOUND_ERROR_MSG.encode() in response.data


def test_api_response_on_success_returns_list_translations(client) -> None:
    language = LanguageFactory()
    translations = TranslationFactory.create_batch(size=5, language=language)
    url = url_for(
        "translations.translation_detail_api_by_language", language_id=language.id
    )

    response = client.get(url)

    assert 200 == response.status_code
    assert len(translations) == len(response.get_json()["translations"])

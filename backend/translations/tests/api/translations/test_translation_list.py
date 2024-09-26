from tests.factories import TranslationFactory
from flask import url_for


def test_api_response_on_success_returns_list_dtos_of_all_translations(client) -> None:
    translations = TranslationFactory.create_batch(5)
    url = url_for("translations.translation_list")

    response = client.get(url)

    assert 200 == response.status_code
    assert len(translations) == len(response.get_json()["translations"])

from tests.factory import TranslationFactory
from flask import url_for
from flask.testing import Client


class TestGetAllTranslations:

    def test_when_no_translations(self, client: Client) -> None:
        response = client.get(url_for("translations.get_all_translations"))
        assert 200 == response.status_code
        assert {"translations": []} == response.json

    def test_when_translations_found(self, client: Client) -> None:
        translations = TranslationFactory.create_batch(5)

        response = client.get(url_for("translations.get_all_translations"))

        assert 200 == response.status_code
        assert len(translations) == len(response.json["translations"])

from tests.factory import TranslationFactory
from translations.api.exceptions import EntityNotFoundError
from flask import url_for
from flask.testing import Client


class TestGetTranslationById:

    def test_when_translation_not_found(self, client: Client) -> None:
        response = client.get(
            url_for('translations.get_translation_by_id', translation_id=999))
        assert 400 == response.status_code
        assert { 'message': EntityNotFoundError('Translation not found').message } == response.json

    def test_when_translation_found(self, client: Client) -> None:
        translation = TranslationFactory()

        response = client.get(
            url_for('translations.get_translation_by_id', translation_id=translation.id))

        assert 200 == response.status_code
        assert translation.id == response.json['id']

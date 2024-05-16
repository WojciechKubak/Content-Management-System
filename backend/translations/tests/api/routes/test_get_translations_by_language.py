from tests.factory import TranslationFactory, LanguageFactory
from translations.api.exceptions import EntityNotFoundError
from flask import url_for
from flask.testing import Client


class TestGetTranslationsByLanguage:

    def test_when_language_not_found(self, client: Client) -> None:
        response = client.get(
            url_for('translations.get_translations_by_language', language_id=999))
        assert 400 == response.status_code
        assert { 'message': EntityNotFoundError('Language not found').message } == response.json

    def test_when_translations_found(self, client: Client) -> None:
        language = LanguageFactory()
        translations = TranslationFactory.create_batch(5, language=language)

        response = client.get(
            url_for('translations.get_translations_by_language', language_id=language.id))

        assert 200 == response.status_code
        assert len(translations) == len(response.json['translations'])

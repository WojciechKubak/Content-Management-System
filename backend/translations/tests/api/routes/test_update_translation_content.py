from tests.factory import TranslationFactory
from translations.persistance.entity import StatusType
from translations.api.exceptions import EntityNotFoundError, MissingDataError, TranslationNotPendingError
from flask import url_for
from flask.testing import Client


class TestUpdateTranslationContent:

    def test_when_no_content_provided(self, client: Client) -> None:
        translation = TranslationFactory()

        response = client.put(
            url_for('translations.update_translation_content', translation_id=translation.id), 
            json={'content': ''}
        )

        assert 400 == response.status_code
        assert { 'message': MissingDataError().message } == response.json

    def test_when_not_found(self, client: Client) -> None:
        response = client.put(
            url_for('translations.update_translation_content', translation_id=999), 
            json={'content': 'new content'}
        )

        assert 400 == response.status_code
        assert { 'message': EntityNotFoundError('Translation not found').message } == response.json

    def test_when_not_pending(self, client: Client) -> None:
        translation = TranslationFactory(status=StatusType.REQUESTED)

        response = client.put(
            url_for('translations.update_translation_content', translation_id=translation.id),
            json={'content': 'new content'}
        )

        assert 400 == response.status_code
        assert { 'message': TranslationNotPendingError().message } == response.json

    def test_when_translation_updated(self, client: Client) -> None:
        translation = TranslationFactory()
        new_content = 'new content'

        response = client.put(
            url_for('translations.update_translation_content', translation_id=translation.id),
            json={'content': new_content}
        )

        assert 200 == response.status_code
        assert new_content == response.json['translation_content']

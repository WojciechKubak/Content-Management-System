from tests.factory import TranslationFactory
from translations.api.exceptions import (
    EntityNotFoundError, 
    InvalidRedactorIdError, 
    TranslationAlreadyReleasedError,
    InvalidStatusOperationError
)
from translations.persistance.entity import StatusType
from flask import url_for
from flask.testing import Client


class TestUpdateTranslationStatus:

    def test_when_translation_not_found(self, client: Client) -> None:
        response = client.put(
            url_for('translations.update_translation_status', translation_id=999), 
            json={'status': StatusType.COMPLETED.value, 'redactor_id': 1}
        )

        assert 400 == response.status_code
        assert { 'message': EntityNotFoundError('Translation not found').message } == response.json

    def test_when_invalid_redactor_provided(self, client: Client) -> None:
        translation = TranslationFactory()

        response = client.put(
            url_for('translations.update_translation_status', translation_id=translation.id), 
            json={'status': StatusType.COMPLETED.value, 'redactor_id': -999}
        )

        assert 400 == response.status_code
        assert { 'message': InvalidRedactorIdError().message } == response.json

    def test_when_invalid_status_provided(self, client: Client) -> None:
        translation = TranslationFactory()

        response = client.put(
            url_for('translations.update_translation_status', translation_id=translation.id), 
            json={'status': f"{StatusType.COMPLETED.value}_invalid", 'redactor_id': 1}
        )

        assert 400 == response.status_code
        assert { 'message': InvalidStatusOperationError().message } == response.json

    def test_when_translation_already_released(self, client: Client) -> None:
        translation = TranslationFactory(status=StatusType.RELEASED)

        response = client.put(
            url_for('translations.update_translation_status', translation_id=translation.id), 
            json={'status': StatusType.COMPLETED.value, 'redactor_id': 1})
        
        assert 400 == response.status_code
        assert { 'message': TranslationAlreadyReleasedError().message } == response.json

    def test_when_status_updated(self, client: Client) -> None:
        translation = TranslationFactory(status=StatusType.PENDING)

        response = client.put(
            url_for('translations.update_translation_status', translation_id=translation.id),
            json={'status': StatusType.COMPLETED.value, 'redactor_id': 1}
        )

        assert 200 == response.status_code
        assert StatusType.COMPLETED.value == response.json['status']

from tests.factory import TranslationFactory
from translations.persistance.entity import StatusType
from translations.api.exceptions import (
    EntityNotFoundError,
    MissingDataError,
    TranslationNotPendingError,
)
from flask import url_for
from flask.testing import Client


class TestUpdateTranslationTitle:

    def test_when_no_title_provided(self, client: Client) -> None:
        translation = TranslationFactory()

        response = client.put(
            url_for(
                "translations.update_translation_title", translation_id=translation.id
            ),
            json={"title": ""},
        )

        assert 400 == response.status_code
        assert {"message": MissingDataError().message} == response.json

    def test_when_translation_not_found(self, client: Client) -> None:
        response = client.put(
            url_for("translations.update_translation_title", translation_id=999),
            json={"title": "new title"},
        )

        assert 400 == response.status_code
        assert {
            "message": EntityNotFoundError("Translation not found").message
        } == response.json

    def test_when_translation_not_pending(self, client: Client) -> None:
        translation = TranslationFactory(status=StatusType.RELEASED)

        response = client.put(
            url_for(
                "translations.update_translation_title", translation_id=translation.id
            ),
            json={"title": "new title"},
        )

        assert 400 == response.status_code
        assert {"message": TranslationNotPendingError().message} == response.json

    def test_when_translation_updated(self, client: Client) -> None:
        translation = TranslationFactory()
        new_title = "new title"

        response = client.put(
            url_for(
                "translations.update_translation_title", translation_id=translation.id
            ),
            json={"title": new_title},
        )

        assert 200 == response.status_code
        assert new_title == response.json["translation_title"]

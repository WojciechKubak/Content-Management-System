from translations.api.service import ApiService
from translations.gpt.exceptions import ChatGptServiceError
from tests.factory import TranslationFactory, StatusType
from translations.api.exceptions import EntityNotFoundError, TranslationNotPendingError
from flask import url_for
from flask.testing import Client
from unittest.mock import patch


class TestGenerateContentTranslation:

    def test_when_translation_not_found(self, client: Client) -> None:
        response = client.post(
            url_for("translations.generate_content_translation", translation_id=999)
        )
        assert 400 == response.status_code
        assert {
            "message": EntityNotFoundError("Translation not found").message
        } == response.json

    def test_when_status_not_pending(self, client: Client) -> None:
        translation = TranslationFactory(status=StatusType.COMPLETED)

        response = client.post(
            url_for(
                "translations.generate_content_translation",
                translation_id=translation.id,
            )
        )

        assert 400 == response.status_code
        assert {"message": TranslationNotPendingError().message} == response.json

    def test_when_gpt_service_error(
        self, client: Client, api_service: ApiService
    ) -> None:
        translation = TranslationFactory()

        with patch.object(
            api_service.chat_gpt_service,
            "get_translation",
            side_effect=ChatGptServiceError,
        ):
            response = client.post(
                url_for(
                    "translations.generate_content_translation",
                    translation_id=translation.id,
                )
            )

        assert 400 == response.status_code
        assert {"message": ChatGptServiceError().message} == response.json

    def test_when_translated(self, client: Client) -> None:
        translation = TranslationFactory()

        response = client.post(
            url_for(
                "translations.generate_content_translation",
                translation_id=translation.id,
            )
        )

        assert 200 == response.status_code
        assert (
            f"TRANSLATED CONTENT OF {translation.article.content_path}"
            == response.json["content"]
        )

from tests.factory import TranslationFactory
from translations.api.exceptions import EntityNotFoundError, TranslationNotPendingError
from translations.api.service import ApiService
from translations.persistance.entity import StatusType
import pytest


class TestTranslateContent:

    def test_when_no_article(self, api_service: ApiService) -> None:
        with pytest.raises(EntityNotFoundError) as e:
            api_service.translate_content(999)
        assert EntityNotFoundError("Translation not found").message == str(e.value)

    def test_when_not_pending(self, api_service: ApiService) -> None:
        translation = TranslationFactory(status=StatusType.REQUESTED)

        with pytest.raises(TranslationNotPendingError) as e:
            api_service.translate_content(translation.id)

        assert "Translation is not pending" == str(e.value)

    def test_when_translation_generated(self, api_service: ApiService) -> None:
        translation = TranslationFactory()
        result = api_service.translate_content(translation.id)
        assert f"TRANSLATED CONTENT OF {translation.article.content_path}" == result

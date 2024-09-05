from tests.factory import TranslationFactory
from translations.api.exceptions import MissingDataError, EntityNotFoundError, TranslationNotPendingError
from translations.persistance.entity import StatusType
from translations.api.service import ApiService
import pytest


class TestChangeTranslationContent:

    def test_change_when_no_content(self, api_service: ApiService) -> None:
        translation = TranslationFactory()

        with pytest.raises(MissingDataError) as e:
            api_service.change_translation_content(translation.id, '')

        assert MissingDataError().message == str(e.value)

    def test_when_no_translation(self, api_service: ApiService) -> None:
        with pytest.raises(EntityNotFoundError) as e:
            api_service.change_translation_content(999, 'test content')
        assert EntityNotFoundError('Translation not found').message == str(e.value)

    def test_when_not_pending(self, api_service: ApiService) -> None:
        translation = TranslationFactory(status=StatusType.REQUESTED)

        with pytest.raises(TranslationNotPendingError) as e:
            api_service.change_translation_content(translation.id, 'test content')
        assert TranslationNotPendingError().message == str(e.value)

    def test_when_content_changed(self, api_service: ApiService) -> None:
        translation = TranslationFactory()

        new_content = "new content"
        result = api_service.change_translation_content(translation.id, new_content)

        assert new_content == result.translation_content

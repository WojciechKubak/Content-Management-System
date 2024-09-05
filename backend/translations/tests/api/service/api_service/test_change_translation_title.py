from tests.factory import TranslationFactory
from translations.api.exceptions import MissingDataError, EntityNotFoundError, TranslationNotPendingError
from translations.persistance.entity import StatusType, Translation, sa
from translations.api.service import ApiService
import pytest


class TestChangeTranslationTitle:

    def test_change_when_no_content(self, api_service: ApiService) -> None:
        translation = TranslationFactory()

        with pytest.raises(MissingDataError) as e:
            api_service.change_translation_title(translation.id, '')

        assert MissingDataError().message == str(e.value)

    def test_when_no_translation(self, api_service: ApiService) -> None:
        with pytest.raises(EntityNotFoundError) as e:
            api_service.change_translation_title(999, 'test title')
        assert EntityNotFoundError('Translation not found').message == str(e.value)

    def test_when_not_pending(self, api_service: ApiService) -> None:
        translation = TranslationFactory(status=StatusType.REQUESTED)

        with pytest.raises(TranslationNotPendingError) as e:
            api_service.change_translation_title(translation.id, 'test title')

        assert TranslationNotPendingError().message == str(e.value)

    def test_when_title_changed(self, api_service: ApiService) -> None:
        translation = TranslationFactory()

        new_title = f"new {translation.title}"
        api_service.change_translation_title(translation.id, f"new {translation.title}")

        assert new_title == sa.session.query(Translation).filter_by(id=translation.id).first().title

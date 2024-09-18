from tests.factory import TranslationFactory
from translations.api.exceptions import (
    EntityNotFoundError,
    InvalidRedactorIdError,
    InvalidStatusOperationError,
    TranslationAlreadyReleasedError,
)
from translations.persistance.entity import StatusType, Translation, sa
from translations.api.service import ApiService
import pytest


class TestChangeTranslationStatus:

    def test_when_no_translation(self, api_service: ApiService) -> None:
        with pytest.raises(EntityNotFoundError) as e:
            api_service.change_translation_status(1, "REQUESTED", 1)
        assert EntityNotFoundError("Translation not found").message == str(e.value)

    def test_when_invalid_redactor_id(self, api_service: ApiService) -> None:
        translation = TranslationFactory()

        with pytest.raises(InvalidRedactorIdError) as e:
            api_service.change_translation_status(translation.id, "REQUESTED", -1)

        assert InvalidRedactorIdError().message == str(e.value)

    def test_when_invalid_status_value(self, api_service: ApiService) -> None:
        translation = TranslationFactory()

        with pytest.raises(InvalidStatusOperationError) as e:
            api_service.change_translation_status(
                translation.id, f"INVALID {translation.status}", 1
            )

        assert InvalidStatusOperationError().message == str(e.value)

    def test_when_already_released(self, api_service: ApiService) -> None:
        translation = TranslationFactory(status=StatusType.RELEASED)

        with pytest.raises(TranslationAlreadyReleasedError) as e:
            api_service.change_translation_status(translation.id, "REQUESTED", 1)

        assert TranslationAlreadyReleasedError().message == str(e.value)

    def test_when_status_changed(self, api_service: ApiService) -> None:
        translation = TranslationFactory()
        api_service.change_translation_status(
            translation.id, StatusType.COMPLETED.value, 1
        )
        assert (
            sa.session.query(Translation).filter_by(id=translation.id).first().status
            == StatusType.COMPLETED
        )

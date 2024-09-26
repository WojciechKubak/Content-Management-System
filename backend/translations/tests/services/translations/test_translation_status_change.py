from translations.services.translations import (
    TRANSLATION_NOT_FOUND_ERROR_MSG,
    TRANSLATION_ALREADY_RELEASED_ERROR_MSG,
    TRANSLATED_ARTICLES_TOPIC,
    ListTranslationDTO,
    TranslationResponse,
    ValidationError,
    Translation,
    translation_status_change,
)
from unittest.mock import MagicMock
import pytest


def test_translation_status_change_raises_validation_error_on_missing_translation(
    mock_translation_repository,
) -> None:
    mock_translation_repository.find_by_id.return_value = None

    with pytest.raises(ValidationError, match=TRANSLATION_NOT_FOUND_ERROR_MSG):
        translation_status_change(
            translation_id=1, status=Translation.StatusType.COMPLETED, redactor_id=1
        )

    mock_translation_repository.find_by_idassert_called_once_with(1)


def test_translation_status_change_raises_validation_error_on_released_status(
    mock_translation_repository,
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.RELEASED
    mock_translation_repository.find_by_id.return_value = mock_translation

    with pytest.raises(ValidationError, match=TRANSLATION_ALREADY_RELEASED_ERROR_MSG):
        translation_status_change(
            translation_id=1, status=Translation.StatusType.COMPLETED, redactor_id=1
        )

    mock_translation_repository.find_by_id.assert_called_once_with(1)


def test_translation_status_change_to_requested_updates_instance_and_resets_translator(
    mock_translation_repository,
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.REQUESTED
    mock_translation.translator_id = 1

    mock_translation_repository.find_by_id.return_value = mock_translation

    result = translation_status_change(
        translation_id=1, status="requested", redactor_id=1
    )

    mock_translation_repository.find_by_id.assert_called_once_with(1)
    assert mock_translation.translator_id is None
    assert Translation.StatusType.REQUESTED == mock_translation.status
    mock_translation_repository.save_or_update.assert_called_once_with(mock_translation)
    assert ListTranslationDTO.from_entity(mock_translation) == result


def test_translation_status_change_to_pending_updates_instance_and_assigns_translator(
    mock_translation_repository,
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.REQUESTED
    mock_translation.translator_id = None

    mock_translation_repository.find_by_id.return_value = mock_translation

    result = translation_status_change(
        translation_id=1, status="pending", redactor_id=1
    )

    mock_translation_repository.find_by_id.assert_called_once_with(1)
    assert 1 == mock_translation.translator_id
    assert Translation.StatusType.PENDING == mock_translation.status
    mock_translation_repository.save_or_update.assert_called_once_with(mock_translation)
    assert ListTranslationDTO.from_entity(mock_translation) == result


def test_translation_status_change_to_completed_updates_instance(
    mock_translation_repository,
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.REQUESTED

    mock_translation_repository.find_by_id.return_value = mock_translation

    result = translation_status_change(
        translation_id=1, status="completed", redactor_id=1
    )

    mock_translation_repository.find_by_id.assert_called_once_with(1)
    assert Translation.StatusType.COMPLETED == mock_translation.status
    mock_translation_repository.save_or_update.assert_called_once_with(mock_translation)
    assert ListTranslationDTO.from_entity(mock_translation) == result


def test_translation_status_change_to_released_updates_instance_and_produces_broker_message(
    mock_translation_repository, mock_message_produce
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.REQUESTED

    mock_translation_repository.find_by_id.return_value = mock_translation

    result = translation_status_change(
        translation_id=1, status="released", redactor_id=1
    )

    mock_translation_repository.find_by_id.assert_called_once_with(1)
    assert Translation.StatusType.RELEASED == mock_translation.status
    mock_message_produce.assert_called_once_with(
        TRANSLATED_ARTICLES_TOPIC, TranslationResponse.from_entity(mock_translation)
    )
    mock_translation_repository.save_or_update.assert_called_once_with(mock_translation)
    assert ListTranslationDTO.from_entity(mock_translation) == result


def test_translation_status_change_to_rejected_updates_instance_and_resets_translator(
    mock_translation_repository,
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.REQUESTED
    mock_translation.translator_id = 1
    mock_translation_repository.find_by_id.return_value = mock_translation

    result = translation_status_change(
        translation_id=1, status="rejected", redactor_id=1
    )

    mock_translation_repository.find_by_id.assert_called_once_with(1)
    assert mock_translation.translator_id is None
    assert Translation.StatusType.REJECTED == mock_translation.status
    mock_translation_repository.save_or_update.assert_called_once_with(mock_translation)
    assert ListTranslationDTO.from_entity(mock_translation) == result

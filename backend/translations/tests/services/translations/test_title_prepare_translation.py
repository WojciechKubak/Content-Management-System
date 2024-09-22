from translations.services.translations import (
    TRANSLATION_NOT_FOUND_ERROR_MSG,
    TRANSLATION_NOT_PENDING_ERROR_MSG,
    TitleTranslationRequest,
    ValidationError,
    Translation,
    title_prepare_translation,
)
from unittest.mock import MagicMock
import pytest


def test_title_prepare_translation_raises_validation_error_on_missing_translation(
    mock_translation_repository,
) -> None:
    mock_translation_repository.find_by_id.return_value = None

    with pytest.raises(ValidationError, match=TRANSLATION_NOT_FOUND_ERROR_MSG):
        title_prepare_translation(translation_id=1)

    mock_translation_repository.find_by_id.assert_called_once_with(1)


def test_title_prepare_translation_raises_validation_error_on_not_pending_status(
    mock_translation_repository,
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.COMPLETED
    mock_translation_repository.find_by_id.return_value = mock_translation

    with pytest.raises(ValidationError, match=TRANSLATION_NOT_PENDING_ERROR_MSG):
        title_prepare_translation(translation_id=1)

    mock_translation_repository.find_by_id.assert_called_once_with(1)


def test_title_prepare_translation_on_success_calls_translation_prepare_and_returns_translated_title(
    mock_translation_repository, mock_get_translation
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.PENDING
    mock_translation.title = "Title"
    mock_translation.article.content_path = "path/filename.txt"
    mock_translation.language = MagicMock()
    mock_translation_repository.find_by_id.return_value = mock_translation

    result = title_prepare_translation(translation_id=1)
    expected_request = TitleTranslationRequest(
        mock_translation.title, mock_translation.language
    )

    mock_get_translation.assert_called_once_with(request=expected_request)
    assert mock_get_translation(expected_request) == result

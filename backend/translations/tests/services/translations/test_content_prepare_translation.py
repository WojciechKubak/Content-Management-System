from translations.services.translations import (
    TRANSLATION_NOT_FOUND_ERROR_MSG,
    TRANSLATION_NOT_PENDING_ERROR_MSG,
    ContentTranslationRequest,
    ValidationError,
    Translation,
    content_prepare_translation,
)
from unittest.mock import MagicMock
import pytest


def test_content_prepare_translation_raises_validation_error_on_missing_translation(
    mock_translation_repository,
) -> None:
    mock_translation_repository.find_by_id.return_value = None

    with pytest.raises(ValidationError, match=TRANSLATION_NOT_FOUND_ERROR_MSG):
        content_prepare_translation(translation_id=1)

    mock_translation_repository.find_by_id.assert_called_once_with(1)


def test_content_prepare_translation_raises_validation_error_on_not_pending_status(
    mock_translation_repository,
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.COMPLETED
    mock_translation_repository.find_by_id.return_value = mock_translation

    with pytest.raises(ValidationError, match=TRANSLATION_NOT_PENDING_ERROR_MSG):
        content_prepare_translation(translation_id=1)

    mock_translation_repository.find_by_id.assert_called_once_with(1)


def test_content_prepare_translation_on_success_calls_translation_prepare_and_returns_content(
    mock_translation_repository, mock_get_content, mock_get_translation
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.PENDING
    mock_translation.article.content_path = "path/filename.txt"
    mock_translation.language = MagicMock()
    mock_translation_repository.find_by_id.return_value = mock_translation

    result = content_prepare_translation(translation_id=1)

    expected_content = mock_get_content.side_effect(
        mock_translation.article.content_path
    )
    expected_request = ContentTranslationRequest(
        content=expected_content, language=mock_translation.language
    )

    mock_get_content.assert_called_once_with(
        file_name=mock_translation.article.content_path
    )
    mock_get_translation.assert_called_once_with(request=expected_request)
    assert mock_get_translation(expected_request) == result

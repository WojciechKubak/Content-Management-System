from translations.services.translations import (
    TRANSLATION_NOT_FOUND_ERROR_MSG,
    TRANSLATION_NOT_PENDING_ERROR_MSG,
    TranslationDTO,
    ValidationError,
    Translation,
    translation_content_change,
)
from unittest.mock import MagicMock
import pytest


def test_translation_content_change_raises_validation_error_on_missing_translation(
    mock_translation_repository,
) -> None:
    mock_translation_repository.find_by_id.return_value = None

    with pytest.raises(ValidationError, match=TRANSLATION_NOT_FOUND_ERROR_MSG):
        translation_content_change(translation_id=1, new_content="text")

    mock_translation_repository.find_by_id.assert_called_once_with(1)


def test_translation_content_change_raises_validation_error_on_not_pending_status(
    mock_translation_repository,
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.COMPLETED
    mock_translation_repository.find_by_id.return_value = mock_translation

    with pytest.raises(ValidationError, match=TRANSLATION_NOT_PENDING_ERROR_MSG):
        translation_content_change(translation_id=1, new_content="text")

    mock_translation_repository.find_by_id.assert_called_once_with(1)


def test_translation_content_change_on_success_creates_new_txt_file_with_content(
    mock_translation_repository, mock_file_upload, mock_get_content
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.PENDING
    mock_translation.content_path = None
    mock_translation.article.content_path = "path/file_name.txt"
    mock_translation_repository.find_by_id.return_value = mock_translation

    result = translation_content_change(translation_id=1, new_content="text")

    mock_file_upload.assert_called_once()
    assert "file_name" in mock_file_upload.call_args[1]
    assert "text" == mock_file_upload.call_args[1]["content"]
    mock_translation_repository.save_or_update.assert_called_once_with(mock_translation)
    mock_get_content.assert_called_once_with(
        file_name=mock_translation.article.content_path
    )
    expected_content = mock_get_content.side_effect(
        mock_translation.article.content_path
    )
    assert TranslationDTO.from_entity(mock_translation).with_contents(
        expected_content, "text" == result
    )


def test_translation_change_on_success_updates_existing_txt_file_with_new_content(
    mock_translation_repository, mock_file_upload, mock_get_content
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.PENDING
    mock_translation.content_path = None
    mock_translation.article.content_path = "path1/file_name.txt"
    mock_translation.content_path = "path2/file_name.txt"
    mock_translation_repository.find_by_id.return_value = mock_translation

    result = translation_content_change(translation_id=1, new_content="text")

    expected_content = mock_get_content.side_effect(
        mock_translation.article.content_path
    )
    expected = TranslationDTO.from_entity(mock_translation).with_contents(
        expected_content, "text"
    )

    mock_file_upload.assert_called_once_with(
        file_name=mock_translation.content_path, content="text"
    )
    mock_get_content.assert_called_once_with(
        file_name=mock_translation.article.content_path
    )
    assert expected == result

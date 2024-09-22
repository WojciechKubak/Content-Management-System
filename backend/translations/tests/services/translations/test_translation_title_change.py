from translations.services.translations import (
    TRANSLATION_NOT_FOUND_ERROR_MSG,
    TRANSLATION_NOT_PENDING_ERROR_MSG,
    TranslationDTO,
    ValidationError,
    Translation,
    translation_title_change,
)
from unittest.mock import MagicMock, call
import pytest


def test_translation_title_change_raises_validation_error_on_missing_translation(
    mock_translation_repository,
) -> None:
    mock_translation_repository.find_by_id.return_value = None

    with pytest.raises(ValidationError, match=TRANSLATION_NOT_FOUND_ERROR_MSG):
        translation_title_change(translation_id=1, new_title="Title")

    mock_translation_repository.find_by_id.assert_called_once_with(1)


def test_translation_title_change_raises_validation_error_on_not_pending_status(
    mock_translation_repository,
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.RELEASED

    mock_translation_repository.find_by_id.return_value = mock_translation

    with pytest.raises(ValidationError, match=TRANSLATION_NOT_PENDING_ERROR_MSG):
        translation_title_change(translation_id=1, new_title="Title")

    mock_translation_repository.find_by_id.assert_called_once_with(1)


def test_translation_title_change_on_success_gets_content_and_returns_translation_dto(
    mock_translation_repository, mock_get_content
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.status = Translation.StatusType.PENDING
    mock_translation.content_path = "path1/file_name.txt"
    mock_translation.article.content_path = "path2/file_name.txt"
    mock_translation_repository.find_by_id.return_value = mock_translation

    result = translation_title_change(translation_id=1, new_title="Title")

    expected_translated = mock_get_content.side_effect(mock_translation.content_path)
    expected_original = mock_get_content.side_effect(
        mock_translation.article.content_path
    )
    expected = TranslationDTO.from_entity(mock_translation).with_contents(
        expected_original, expected_translated
    )

    mock_translation_repository.find_by_id.assert_called_once_with(1)
    mock_translation_repository.save_or_update.assert_called_once_with(mock_translation)
    mock_get_content.assert_has_calls(
        [
            call(file_name=mock_translation.content_path),
            call(file_name=mock_translation.article.content_path),
        ],
        any_order=True,
    )
    assert expected == result

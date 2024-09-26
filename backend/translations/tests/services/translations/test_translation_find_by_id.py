from translations.services.translations import (
    TRANSLATION_NOT_FOUND_ERROR_MSG,
    TranslationDTO,
    ValidationError,
    Translation,
    translation_find_by_id,
)
from unittest.mock import MagicMock, call
import pytest


def test_translation_find_by_id_raises_validation_error_on_missing_translation(
    mock_translation_repository,
) -> None:
    mock_translation_repository.find_by_id.return_value = None

    with pytest.raises(ValidationError, match=TRANSLATION_NOT_FOUND_ERROR_MSG):
        translation_find_by_id(translation_id=1)

    mock_translation_repository.find_by_id.assert_called_once_with(1)


def test_translation_find_by_id_on_success_returns_translation_dto_with_loaded_content(
    mock_translation_repository, mock_get_content
) -> None:
    mock_translation = MagicMock(spec=Translation)
    mock_translation.article.content_path = "path1/file_name.txt"
    mock_translation.content_path = "path2/file_name.txt"
    mock_translation_repository.find_by_id.return_value = mock_translation

    result = translation_find_by_id(translation_id=1)

    expected_translated = mock_get_content.side_effect(mock_translation.content_path)
    expected_original = mock_get_content.side_effect(
        mock_translation.article.content_path
    )
    expected = TranslationDTO.from_entity(mock_translation).with_contents(
        expected_original, expected_translated
    )

    mock_translation_repository.find_by_id.assert_called_once_with(1)
    mock_get_content.assert_has_calls(
        [
            call(file_name=mock_translation.article.content_path),
            call(file_name=mock_translation.content_path),
        ],
        any_order=True,
    )
    assert expected == result

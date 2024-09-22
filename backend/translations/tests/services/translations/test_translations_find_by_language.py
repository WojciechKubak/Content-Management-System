from translations.services.translations import (
    LANGUAGE_NOT_FOUND_ERROR_MSG,
    ListTranslationDTO,
    ValidationError,
    Translation,
    translations_find_by_language,
)
from unittest.mock import MagicMock
import pytest


def test_translation_find_by_language_raises_validation_error_on_missing_language(
    mock_language_repository,
) -> None:
    mock_language_repository.find_by_id.return_value = None

    with pytest.raises(ValidationError, match=LANGUAGE_NOT_FOUND_ERROR_MSG):
        translations_find_by_language(language_id=1)

    mock_language_repository.find_by_id.assert_called_once_with(1)


def test_translation_find_by_language_on_success_returns_list_of_translation_dtos(
    mock_language_repository,
    mock_translation_repository,
) -> None:
    mock_language_repository.find_by_id = MagicMock()

    mock_translations = [MagicMock(spec=Translation) for _ in range(3)]
    mock_translation_repository.find_by_language.return_value = mock_translations

    result = translations_find_by_language(language_id=1)
    expected = [ListTranslationDTO.from_entity(mock) for mock in mock_translations]

    mock_language_repository.find_by_id.assert_called_once_with(1)
    mock_translation_repository.find_by_language.assert_called_once_with(1)
    assert expected == result

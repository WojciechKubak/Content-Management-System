from translations.services.translations import (
    ListTranslationDTO,
    Translation,
    translations_get_all,
)
from unittest.mock import MagicMock


def test_translation_get_all_returns_list_of_translation_dtos(
    mock_translation_repository,
) -> None:
    mock_translations = [MagicMock(spec=Translation) for _ in range(3)]
    mock_translation_repository.find_all.return_value = mock_translations

    result = translations_get_all()
    expected = [ListTranslationDTO.from_entity(mock) for mock in mock_translations]

    mock_translation_repository.find_all.assert_called_once_with(limit=10, offset=0)
    assert expected == result

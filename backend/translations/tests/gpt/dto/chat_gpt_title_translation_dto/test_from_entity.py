from translations.gpt.dto import ChatGptTitleTranslationDTO
from unittest.mock import MagicMock


def test_from_dto() -> None:
    mock_translation = MagicMock()
    mock_translation.language.name = "test language"
    mock_translation.article.title = "test title"

    result = ChatGptTitleTranslationDTO.from_entity(mock_translation)

    assert mock_translation.language.name == result.language
    assert mock_translation.article.title == result.text
    assert "user" == result.role

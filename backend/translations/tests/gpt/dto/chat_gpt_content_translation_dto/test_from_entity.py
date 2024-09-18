from translations.gpt.dto import ChatGptContentTranslationDTO
from unittest.mock import MagicMock


def test_from_dto() -> None:
    mock_translation = MagicMock()
    mock_translation.language.name = "test language"
    content = "test content"

    result = ChatGptContentTranslationDTO.from_entity(mock_translation, content)

    assert mock_translation.language.name == result.language
    assert content == result.text
    assert "user" == result.role

from translations.core.exceptions import TranslationError
from translations.integrations.gpt.client import (
    ContentTranslationRequest,
    content_get_translation,
)
from openai import OpenAIError
from unittest.mock import patch, MagicMock
from typing import Generator
import pytest


@pytest.fixture
def mock_openai_client() -> Generator:
    with patch("translations.integrations.gpt.client.OpenAI") as mock_client:
        yield mock_client


def test_content_get_translation_success(mock_openai_client) -> None:
    mock_openai = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="translated content"))]
    mock_openai.chat.completions.create.return_value = mock_response
    mock_openai_client.return_value = mock_openai

    request = ContentTranslationRequest(content="test content", language="fr")
    result = content_get_translation(request=request)

    mock_openai.chat.completions.create.assert_called_once_with(
        messages=[{"role": request.role, "content": str(request)}],
        model="gpt-3.5-turbo",
    )
    assert result == "translated content"


def test_content_get_translation_failure(mock_openai_client) -> None:
    mock_openai = MagicMock()
    mock_openai.chat.completions.create.side_effect = OpenAIError
    mock_openai_client.return_value = mock_openai

    request = ContentTranslationRequest(content="test content", language="fr")

    with pytest.raises(TranslationError, match="Failed to translate content"):
        content_get_translation(request=request)

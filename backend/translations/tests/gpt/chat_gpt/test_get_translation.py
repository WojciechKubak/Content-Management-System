from translations.gpt.chat_gpt import ChatGPTService
from translations.gpt.exceptions import ChatGptServiceError
from translations.gpt.dto import ChatGptTitleTranslationDTO
from unittest.mock import patch
from unittest.mock import MagicMock, patch
from openai import OpenAIError
import pytest


class TestGetTranslation:
    translation_request_dto = ChatGptTitleTranslationDTO(
        text="translation_title", language="language"
    )

    @patch("translations.gpt.chat_gpt.OpenAI", new_callable=MagicMock)
    def test_when_error_occurs(self, mock_openai_class) -> None:
        mock_openai_instance = mock_openai_class.return_value
        mock_openai_instance.chat.completions.create.side_effect = OpenAIError
        service = ChatGPTService(openai_api_key="test_key")

        with pytest.raises(ChatGptServiceError) as e:
            service.get_translation(self.translation_request_dto)

        assert ChatGptServiceError().message == str(e.value)

    @patch("translations.gpt.chat_gpt.OpenAI", new_callable=MagicMock)
    def test_when_correct(self, mock_openai_class) -> None:
        content = "test_content"
        mock_openai_instance = mock_openai_class.return_value
        mock_openai_instance.chat.completions.create.return_value.choices[
            0
        ].message.content = content
        service = ChatGPTService(openai_api_key="test_key")

        result = service.get_translation(self.translation_request_dto)

        assert content == result

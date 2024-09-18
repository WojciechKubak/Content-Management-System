from translations.gpt.exceptions import ChatGptServiceError
from dataclasses import dataclass
from openai import OpenAI, OpenAIError
from typing import Type


@dataclass
class ChatGPTService:
    """
    A service class for interacting with the OpenAI GPT-3 model.

    Attributes:
        openai_api_key (str): The API key for OpenAI.
    """

    openai_api_key: str

    def __post_init__(self):
        """
        Initializes the OpenAI client with the provided API key.
        """
        self.client = OpenAI(api_key=self.openai_api_key)

    def get_translation(self, translation_request_dto: Type) -> str:
        """
        Sends a translation request to the OpenAI GPT-3 model and returns the response.

        Args:
            translation_request_dto (Type): The data transfer object containing the translation request details.

        Returns:
            str: The translated text.

        Raises:
            ChatGptServiceError: If there's an error in the OpenAI service.
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": translation_request_dto.role,
                        "content": str(translation_request_dto),
                    }
                ],
                model="gpt-3.5-turbo",
            )
            return response.choices[0].message.content
        except OpenAIError:
            raise ChatGptServiceError()

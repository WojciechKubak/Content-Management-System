from translations.common.utils import assert_settings
from translations.core.exceptions import TranslationError
from openai import OpenAI, OpenAIError
from dataclasses import dataclass
from functools import lru_cache
from abc import ABC


@dataclass
class OpenAICredentials:
    api_key: str


@dataclass
class BaseTranslationRequest(ABC):
    content: str
    language: str
    role: str = "user"

    def __str__(self) -> str:
        return f'Translate this title: "{self.content}" to {self.language} language'


@dataclass
class ContentTranslationRequest(BaseTranslationRequest):

    def __str__(self) -> str:
        return super().__str__() + ", keep all tags as they are"


@dataclass
class TitleTranslationRequest(BaseTranslationRequest):
    pass


@lru_cache
def openai_get_credentials() -> OpenAICredentials:
    settings = assert_settings(
        ["OPENAI_API_KEY"],
        "OpenAI credentials not found",
    )
    return OpenAICredentials(api_key=settings["OPENAI_API_KEY"])


def openai_get_client() -> OpenAI:
    credentials = openai_get_credentials()
    return OpenAI(api_key=credentials.api_key)


def content_get_translation(*, request: type[BaseTranslationRequest]) -> str:
    client = openai_get_client()

    try:
        response = client.chat.completions.create(
            messages=[{"role": request.role, "content": str(request)}],
            model="gpt-3.5-turbo",
        )
        return response.choices[0].message.content

    except OpenAIError:
        raise TranslationError("Failed to translate content")

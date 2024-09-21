from translations.integrations.gpt.client import OpenAICredentials
from unittest.mock import patch
from typing import Generator
import pytest


@pytest.fixture
def openai_credentials() -> OpenAICredentials:
    return OpenAICredentials(api_key="test_api_key")


@pytest.fixture(autouse=True)
def patched_openai_get_credentials(openai_credentials) -> Generator:
    with patch(
        "translations.integrations.gpt.client.openai_get_credentials",
        return_value=openai_credentials,
    ):
        yield

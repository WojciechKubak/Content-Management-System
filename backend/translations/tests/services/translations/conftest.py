from typing import Generator
from unittest.mock import patch
import pytest


@pytest.fixture(scope="function", autouse=True)
def mock_message_produce() -> Generator:
    with patch("translations.services.translations.message_produce") as mock:
        yield mock


@pytest.fixture
def mock_translation_repository() -> Generator:
    with patch("translations.services.translations.translation_repository") as mock:
        yield mock


@pytest.fixture
def mock_language_repository() -> Generator:
    with patch("translations.services.translations.language_repository") as mock:
        yield mock

from typing import Generator
from unittest.mock import patch
import pytest


@pytest.fixture
def mock_language_repository():
    with patch("translations.services.handlers.language_repository") as mock:
        yield mock


@pytest.fixture
def mock_article_repository() -> Generator:
    with patch("translations.services.handlers.article_repository") as mock:
        yield mock


@pytest.fixture
def mock_translation_repository() -> Generator:
    with patch("translations.services.handlers.translation_repository") as mock:
        yield mock

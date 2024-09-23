from translations.app import create_app
from translations.config.environments import test
from translations.db.configuration import sa
from translations.db.repositories import TranslationRepository
from flask import Flask
from typing import Generator
from unittest.mock import patch
import pytest


@pytest.fixture
def app() -> Generator:
    yield create_app(test)


@pytest.fixture
def client(app: Flask) -> Generator:
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def db_setup_and_teardown(app: Flask) -> Generator:
    with app.app_context():
        sa.create_all()

        yield app

    with app.app_context():
        sa.drop_all()


@pytest.fixture(autouse=True)
def mock_get_translation() -> Generator:

    def side_effect(request) -> str:
        return f"TRANSLATED ({request.content})"

    with patch("translations.services.translations.get_translation") as mock:
        mock.side_effect = side_effect

        yield mock


@pytest.fixture(autouse=True)
def mock_get_content() -> Generator:

    def side_effect(file_name: str) -> str:
        return f"CONTENT OF ({file_name})"

    with patch("translations.services.translations.get_content") as mock:
        mock.side_effect = side_effect

        yield mock


@pytest.fixture(autouse=True)
def mock_file_upload() -> Generator:

    def side_effect(file_name: str, content: str) -> str:
        return f"CONTENT OF {file_name}: ({content})"

    with patch("translations.services.translations.file_upload") as mock:
        mock.side_effect = side_effect

        yield mock


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


@pytest.fixture
def mock_article_repository() -> Generator:
    with patch("translations.services.translations.article_repository") as mock:
        yield mock


@pytest.fixture(scope="session")
def translation_repository() -> TranslationRepository:
    return TranslationRepository(sa)

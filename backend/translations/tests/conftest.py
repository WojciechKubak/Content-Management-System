from translations.persistance.repository import (
    TranslationRepository,
    LanguageRepository,
    ArticleRepository,
)
from translations.broker.kafka import KafkaService
from backend.translations.translations.storage.client import Boto3Service
from translations.gpt.chat_gpt import ChatGPTService
from translations.persistance.entity import sa
from translations.app import create_app
from translations.config import TestingConfig
from flask import Flask
from flask.testing import Client
from unittest.mock import MagicMock
from typing import Generator
import pytest


@pytest.fixture(scope="function")
def app() -> Generator[Flask, None, None]:
    yield create_app(TestingConfig)


@pytest.fixture(scope="function")
def client(app: Flask) -> Generator[Client, None, None]:
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def db_setup_and_teardown(app: Flask) -> Generator:
    with app.app_context():
        sa.create_all()

        yield app

    with app.app_context():
        sa.drop_all()


@pytest.fixture(scope="session")
def article_repository() -> ArticleRepository:
    return ArticleRepository(sa)


@pytest.fixture(scope="session")
def translation_repository() -> TranslationRepository:
    return TranslationRepository(sa)


@pytest.fixture(scope="session")
def language_repository() -> LanguageRepository:
    return LanguageRepository(sa)


@pytest.fixture(scope="session")
def kafka_service() -> KafkaService:
    mock = MagicMock(spec=KafkaService)
    mock.return_value = None
    return mock


@pytest.fixture(scope="session")
def chat_gpt_service() -> ChatGPTService:
    mock = MagicMock(spec=ChatGPTService)
    mock.get_translation.side_effect = lambda dto: f"TRANSLATED {dto.text}"
    return mock

from translations.app import create_app
from translations.db.configuration import sa
from translations.config.config import TestingConfig
from translations.db.repositories import TranslationRepository
from flask import Flask
from flask.testing import Client
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
def translation_repository() -> TranslationRepository:
    return TranslationRepository(sa)

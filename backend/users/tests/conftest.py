from users.api.service import UserService, CommentService
from users.app import create_app
from users.config import TestingConfig
from users.persistance.configuration import sa
from flask.testing import Client
from flask import Flask
import pytest


@pytest.fixture(scope='function')
def app() -> Flask:
    yield create_app(TestingConfig)


@pytest.fixture(autouse=True)
def db_setup_and_teardown(app: Flask) -> Flask:
    with app.app_context():
        sa.create_all()

        yield app

    with app.app_context():
        sa.drop_all()


@pytest.fixture
def client(app: Flask) -> Client:
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def comment_service() -> CommentService:
    return CommentService()


@pytest.fixture(scope='session')
def user_service() -> UserService:
    return UserService()

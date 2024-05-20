from users.service.user import UserService
from users.service.comment import CommentService
from users.app import create_app
from users.config import TestingConfig
from users.persistance.configuration import sa
from flask.testing import Client
from flask import Flask
from typing import Any, Generator
import pytest


@pytest.fixture(scope='function')
def app() -> Generator[Flask, None, None]:
    yield create_app(TestingConfig)


@pytest.fixture(autouse=True)
def db_setup_and_teardown(app: Flask):
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


@pytest.fixture(scope='session')
def user_dto() -> dict[str, Any]:
    return {
        'username': 'User',
        'email': 'user@example.com',
        'password': '123456'
    }


@pytest.fixture(scope='session')
def comment_dto(user_model_data: dict[str, Any]) -> dict[str, Any]:
    return {
        'content': 'dummy content',
        'article_id': 1,
        'user_id': user_model_data['id']
    }

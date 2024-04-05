from users import create_app
from users.config import TestingConfig
from users.db.configuration import sa
from werkzeug.security import generate_password_hash
from flask.testing import Client
from flask import Flask
from typing import Any
import pytest


@pytest.fixture(scope='function')
def app() -> Flask:
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


@pytest.fixture(scope='session')
def user_model_data(user_dto: dict[str, Any]) -> dict[str, Any]:
    return user_dto | {
        'id': 1,
        'role': 'admin',
        'is_active': False,
        'password': generate_password_hash(user_dto['password'])
    }


@pytest.fixture(scope='session')
def comment_model_data(comment_dto: dict[str, Any]) -> dict[str, Any]:
    return comment_dto | {'id': 1}

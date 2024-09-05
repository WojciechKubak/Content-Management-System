from gateway import create_app
from gateway.config import TestingConfig
from flask import Flask
from flask.testing import FlaskClient
import pytest


@pytest.fixture(scope='function')
def app() -> Flask:
    yield create_app(TestingConfig)


@pytest.fixture(scope='function')
def client(app: Flask) -> FlaskClient:
    with app.test_client() as client:
        yield client

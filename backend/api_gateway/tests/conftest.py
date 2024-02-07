from gateway.app import create_app
from flask.testing import FlaskClient
from flask import Flask
import pytest


@pytest.fixture(scope='session')
def app() -> Flask:
    yield create_app()


@pytest.fixture(scope='session')
def client(app: Flask) -> FlaskClient:
    with app.test_client() as client:
        yield client

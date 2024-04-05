from users.service.user import UserService
from users.email.configuration import MailConfig
from jinja2 import PackageLoader, Environment
from flask import Flask
import pytest


@pytest.fixture(scope='session')
def user_service() -> UserService:
    return UserService()


@pytest.fixture(scope='function')
def app(app: Flask):

    templates_env = Environment(
        loader=PackageLoader('users.email', 'templates'))

    MailConfig.prepare_mail(app, templates_env)

    yield app

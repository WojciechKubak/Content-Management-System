from users.api.exceptions import (
    UserNotFoundException,
    IncorrectPasswordException,
    UserNotActiveException
)
from tests.factory import UserFactory, UserDtoFactory
from flask.testing import Client
from flask import url_for


class TestVerifyCredentials:

    def test_when_user_not_found(self, client: Client) -> None:
        user_dto = UserDtoFactory()

        response = client.post(url_for('users.verify_credentials'), json=user_dto)
        
        assert 400 == response.status_code
        assert {'message': UserNotFoundException().message} == response.json


    def test_when_password_incorrect(self, client: Client) -> None:
        user = UserFactory()
        user_dto = UserDtoFactory(username=user.username, password='incorrect_password')

        response = client.post(url_for('users.verify_credentials'), json=user_dto)
        
        assert 400 == response.status_code
        assert {'message': IncorrectPasswordException().message} == response.json

    def test_when_user_not_active(self, client: Client) -> None:
        user = UserFactory()
        user_dto = UserDtoFactory(username=user.username)

        response = client.post(url_for('users.verify_credentials'), json=user_dto)
        
        assert 400 == response.status_code
        assert {'message': UserNotActiveException().message} == response.json

    def test_when_credentials_verified(self, client: Client) -> None:
        user = UserFactory(is_active=True)
        user_dto = UserDtoFactory(username=user.username)

        response = client.post(url_for('users.verify_credentials'), json=user_dto)
        
        assert 200 == response.status_code
        assert user.id == response.json['id']

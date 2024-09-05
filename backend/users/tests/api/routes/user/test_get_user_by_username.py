from users.api.exceptions import UserNotFoundException
from tests.factory import UserFactory
from flask.testing import Client
from flask import url_for


class TestGetUserByUsername:

    def test_when_user_not_found(self, client: Client) -> None:
        response = client.get(
            url_for('users.get_user_by_username', username='username'))
        assert 400 == response.status_code
        assert {'message': UserNotFoundException().message} == response.json

    def test_when_user_found(self, client: Client) -> None:
        user = UserFactory()

        response = client.get(
            url_for('users.get_user_by_username', username=user.username))
        
        assert 200 == response.status_code
        assert user.username == response.json['username']

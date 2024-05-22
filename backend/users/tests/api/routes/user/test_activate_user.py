from users.api.exceptions import (
    ActivationLinkExpiredException,
    UserNotFoundException,
    UserAlreadyActiveException
)
from tests.factory import UserFactory
from flask.testing import Client
from flask import url_for
from datetime import datetime


class TestActivateUser:
    active_token = datetime.now().timestamp() * 1000 + 10000

    def test_when_link_expired(self, client: Client) -> None:
        user = UserFactory()

        response = client.get(
            url_for('users.activate_user', id=user.id, timestamp=1))
        
        assert 400 == response.status_code
        assert {'message': ActivationLinkExpiredException().message} == response.json

    def test_when_user_not_found(self, client: Client) -> None:
        response = client.get(
            url_for('users.activate_user', id=999, timestamp=self.active_token))
        assert 400 == response.status_code
        assert {'message': UserNotFoundException().message} == response.json

    def test_when_already_active(self, client: Client) -> None:
        user = UserFactory(is_active=True)

        response = client.get(
            url_for('users.activate_user', id=user.id, timestamp=self.active_token))
        
        assert 400 == response.status_code
        assert {'message': UserAlreadyActiveException().message} == response.json  

    def test_when_activated(self, client: Client) -> None:
        user = UserFactory()

        response = client.get(
            url_for('users.activate_user', id=user.id, timestamp=self.active_token))
        
        assert 200 == response.status_code
        assert user.id == response.json['id']
        assert user.is_active == response.json['is_active']

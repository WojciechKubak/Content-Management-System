from users.extensions import sa
from users.model.user import UserModel
from flask.testing import Client
from typing import Any


class TestUserCredentialsResourceGet:

    def test_when_service_error_occurs(self, client: Client) -> None:
        response = client.post('/users/credentials', json={})
        assert 400 == response.status_code
        assert b'User not found' in response.data

    def test_when_credentials_are_correct(self, client: Client, user_dto: dict[str, Any]) -> None:
        user = sa.session.query(UserModel).first()
        user.is_active = True
        sa.session.commit()

        data = {
            'username': user_dto['username'],
            'password': user_dto['password']
        }
        response = client.post('/users/credentials', json=data)
        assert 200 == response.status_code
        assert user_dto['username'] == response.json['username']

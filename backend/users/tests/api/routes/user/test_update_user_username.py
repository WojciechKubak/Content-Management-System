from users.api.exceptions import UserNotFoundException, UserNameInUseException
from tests.factory import UserFactory
from flask.testing import Client
from flask import url_for


class TestUpdateUserRole:

    def test_when_user_not_found(self, client: Client) -> None:
        response = client.put(
            url_for('users.update_user_username', id_=999),
            json={'username': 'username'})
        assert 400 == response.status_code
        assert {'message': UserNotFoundException().message} == response.json

    def test_when_used_username(self, client: Client) -> None:
        user1 = UserFactory()
        user2 = UserFactory()

        response = client.put(
            url_for('users.update_user_username', id_=user1.id),
            json={'username': user2.username})
        
        assert 400 == response.status_code
        assert {'message': UserNameInUseException().message} == response.json

    def test_when_role_updated(self, client: Client) -> None:
        user = UserFactory()
        
        new_username = f'new_{user.username}'
        response = client.put(
            url_for('users.update_user_username', id_=user.id),
            json={'username': new_username})
        
        assert 200 == response.status_code
        assert new_username == response.json['username']

from users.api.exceptions import UserNotFoundException, InvalidRoleException
from users.persistance.entity import UserRoleType
from tests.factory import UserFactory
from flask.testing import Client
from flask import url_for


class TestUpdateUserRole:

    def test_when_user_not_found(self, client: Client) -> None:
        response = client.put(
            url_for('users.update_user_role', id_=999),
            json={'role': 'admin'})
        assert 400 == response.status_code
        assert {'message': UserNotFoundException().message} == response.json

    def test_when_invalid_role(self, client: Client) -> None:
        user = UserFactory()

        response = client.put(
            url_for('users.update_user_role', id_=user.id),
            json={'role': f'invalid_{user.role}'})
        
        assert 400 == response.status_code
        assert {'message': InvalidRoleException().message} == response.json

    def test_when_role_updated(self, client: Client) -> None:
        user = UserFactory()

        new_role = UserRoleType.REDACTOR.value
        response = client.put(
            url_for('users.update_user_role', id_=user.id),
            json={'role': new_role})
        
        assert 200 == response.status_code
        assert new_role == response.json['role']

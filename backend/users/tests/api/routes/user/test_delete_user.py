from users.api.exceptions import UserNotFoundException
from tests.factory import UserFactory
from flask.testing import Client
from flask import url_for


class TestDeleteUser:

    def test_when_user_not_found(self, client: Client) -> None:
        response = client.delete(
            url_for('users.delete_user', id_=999))
        assert 400 == response.status_code
        assert {'message': UserNotFoundException().message} == response.json

    def test_when_user_deleted(self, client: Client) -> None:
        user = UserFactory()

        response = client.delete(
            url_for('users.delete_user', id_=user.id))
        
        assert 200 == response.status_code
        assert {'id': user.id} == response.json
    
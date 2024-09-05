from users.api.exceptions import UserNameInUseException, EmailInUseException
from tests.factory import UserFactory, UserDtoFactory
from flask.testing import Client
from flask import url_for



class TestRegisterUser:

    def test_when_username_already_exists(self, client: Client) -> None:
        user = UserFactory()
        user_dto = UserDtoFactory(username=user.username)

        response = client.post(url_for('users.register_user'), json=user_dto)
        
        assert 400 == response.status_code
        assert {'message': UserNameInUseException().message} == response.json

    def test_when_email_already_exists(self, client: Client) -> None:
        user = UserFactory()
        user_dto = UserDtoFactory(email=user.email)

        response = client.post(url_for('users.register_user'), json=user_dto)
        
        assert 400 == response.status_code
        assert {'message': EmailInUseException().message} == response.json

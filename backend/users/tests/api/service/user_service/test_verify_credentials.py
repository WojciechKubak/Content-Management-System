from users.api.service import UserService
from users.api.service import (
    UserNotFoundException,
    IncorrectPasswordException,
    UserNotActiveException
)
from tests.factory import UserFactory
import pytest


class TestVerifyCredentials:

    def test_when_user_does_not_exist(self, user_service: UserService) -> None:
        with pytest.raises(UserNotFoundException) as e:
            user_service.verify_credentials('username', 'password')
        assert UserNotFoundException().message == str(e.value)

    def test_when_password_is_incorrect(self, user_service: UserService) -> None:
        user = UserFactory()

        with pytest.raises(IncorrectPasswordException) as e:
            user_service.verify_credentials(user.username, 'incorrect_password')

        assert IncorrectPasswordException().message == str(e.value)

    def test_when_user_is_inactive(self, user_service: UserService) -> None:
        user = UserFactory(is_active=False)

        with pytest.raises(UserNotActiveException) as e:
            user_service.verify_credentials(user.username, 'password')

        assert UserNotActiveException().message == str(e.value)

    def test_when_credential_are_correct(self, user_service: UserService) -> None:
        user = UserFactory(is_active=True)
        result = user_service.verify_credentials(user.username, 'password')
        assert user == result

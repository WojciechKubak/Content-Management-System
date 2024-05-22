from users.api.service import UserService
from users.api.service import UserNotFoundException
from tests.factory import UserFactory
import pytest


class TestGetUserById:

    def test_when_user_not_found(self, user_service: UserService) -> None:
        with pytest.raises(UserNotFoundException) as e:
            user_service.get_user_by_id(999)
        assert UserNotFoundException().message == str(e.value)

    def test_when_user_found(self, user_service: UserService) -> None:
        user = UserFactory()
        result = user_service.get_user_by_id(user.id)
        assert result == user

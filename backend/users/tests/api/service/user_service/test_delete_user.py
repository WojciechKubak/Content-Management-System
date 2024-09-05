from users.api.service import UserService
from users.api.service import UserNotFoundException
from users.persistance.entity import User
from tests.factory import UserFactory
import pytest


class TestDeleteUser:

    def test_when_user_not_found(self, user_service: UserService) -> None:
        with pytest.raises(UserNotFoundException) as e:
            user_service.delete_user(999)
        assert UserNotFoundException().message == str(e.value)

    def test_when_deleted(self, user_service: UserService) -> None:
        user = UserFactory()
        user_service.delete_user(user.id)
        assert not User.query.filter_by(id=user.id).first()

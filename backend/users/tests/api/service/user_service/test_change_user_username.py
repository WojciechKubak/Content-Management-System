from users.api.service import UserService
from users.api.service import UserNotFoundException, UserNameInUseException
from users.persistance.entity import User
from tests.factory import UserFactory
import pytest


class TestChangeUserUsername:

    def test_when_user_not_found(self, user_service: UserService) -> None:
        with pytest.raises(UserNotFoundException) as e:
            user_service.change_user_username(999, 'username')
        assert UserNotFoundException().message == str(e.value)

    def test_when_username_in_use(self, user_service: UserService) -> None:
        user = UserFactory()

        with pytest.raises(UserNameInUseException) as e:
            user_service.change_user_username(user.id, user.username)

        assert UserNameInUseException().message == str(e.value)

    def test_when_username_changed(self, user_service: UserService) -> None:
        user = UserFactory()
        new_username = f'new_{user.username}'

        user_service.change_user_username(user.id, new_username)

        assert new_username == User.query.filter_by(id=user.id).first().username

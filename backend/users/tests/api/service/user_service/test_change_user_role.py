from users.api.service import UserService
from users.api.service import UserNotFoundException, InvalidRoleException
from users.persistance.entity import UserRoleType, User
from tests.factory import UserFactory
import pytest


class TestChangeUserRole:
    new_role = UserRoleType.REDACTOR

    def test_when_user_not_found(self, user_service: UserService) -> None:
        with pytest.raises(UserNotFoundException) as e:
            user_service.change_user_role(999, self.new_role.value)
        assert UserNotFoundException().message == str(e.value)

    def test_when_invalid_role(self, user_service: UserService) -> None:
        user = UserFactory()

        with pytest.raises(InvalidRoleException) as e:
            user_service.change_user_role(user.id, f'invalid_{self.new_role.value}')

        assert InvalidRoleException().message == str(e.value)

    def test_when_role_changed(self, user_service: UserService) -> None:
        user = UserFactory()
        user_service.change_user_role(user.id, self.new_role.value)
        assert self.new_role == User.query.filter_by(id=user.id).first().role

from users.api.service import UserService
from users.api.service import UserNameInUseException, EmailInUseException
from users.persistance.entity import User
from tests.factory import UserFactory, UserDtoFactory
import pytest


class TestUserServiceRegisterUser:

    def test_when_username_already_exists(self, user_service: UserService) -> None:
        user_dto = UserDtoFactory()
        UserFactory(
            username=user_dto['username'],
            email=f'other_{user_dto["email"]}',
        )

        with pytest.raises(UserNameInUseException) as e:
            user_service.register_user(user_dto)

        assert UserNameInUseException().message == str(e.value)

    def test_when_email_already_exists(self, user_service: UserService) -> None:
        user_dto = UserDtoFactory()
        UserFactory(
            username=f"other_{user_dto['username']}",
            email=user_dto['email'],
        )

        with pytest.raises(EmailInUseException) as e:
            user_service.register_user(user_dto)

        assert EmailInUseException().message == str(e.value)

    def test_when_registered_succesfully(self, user_service: UserService) -> None:
        user_dto = UserDtoFactory()
        result = user_service.register_user(user_dto)
        assert User.query.filter_by(id=result.id).first()

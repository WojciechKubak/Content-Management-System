from users.api.service import UserService
from users.api.service import (
    ActivationLinkExpiredException,
    UserNotFoundException,
    UserAlreadyActiveException
)
from users.persistance.entity import User
from tests.factory import UserFactory
from datetime import datetime
import pytest


class TestActivateUser:
    valid_token_lifespan = datetime.now().timestamp() * 1000 + 100000

    def test_when_link_expired(self, user_service: UserService) -> None:
        user = UserFactory()

        with pytest.raises(ActivationLinkExpiredException) as e:
            user_service.activate_user(user.id, datetime.now().timestamp() * 1000 - 1)

        assert ActivationLinkExpiredException().message == str(e.value)

    def test_when_user_not_found(self, user_service: UserService) -> None:
        with pytest.raises(UserNotFoundException) as e:
            user_service.activate_user(999, self.valid_token_lifespan)
        assert UserNotFoundException().message == str(e.value)

    def test_when_user_already_active(self, user_service: UserService) -> None:
        user = UserFactory(is_active=True)

        with pytest.raises(UserAlreadyActiveException) as e:
            user_service.activate_user(user.id, self.valid_token_lifespan)
            
        assert UserAlreadyActiveException().message == str(e.value)

    def test_when_user_activated(self, user_service: UserService) -> None:
        user = UserFactory()
        user_service.activate_user(user.id, self.valid_token_lifespan)
        assert User.query.filter_by(id=user.id).first().is_active


from typing import Any


class TestUserCheckPassword:

    def test_when_password_is_incorrect(self, user_model: User, user_dto: dict[str, Any]) -> None:
        incorrect_password = f"{user_dto['password']}1111"
        assert not user_model.check_password(incorrect_password)

    def test_when_password_is_correct(self, user_model: User, user_dto: dict[str, Any]) -> None:
        assert user_model.check_password(user_dto['password'])

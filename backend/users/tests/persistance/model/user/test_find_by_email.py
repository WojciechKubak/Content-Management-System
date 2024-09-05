from users.persistance.entity import User
from tests.factory import UserFactory


def test_find_by_email() -> None:
    user = UserFactory()
    result = User.find_by_email(user.email)
    assert result == user

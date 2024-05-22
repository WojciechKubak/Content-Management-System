from users.persistance.entity import User
from tests.factory import UserFactory


def test_find_by_id() -> None:
    user = UserFactory()
    result = User.find_by_id(user.id)
    assert result == user

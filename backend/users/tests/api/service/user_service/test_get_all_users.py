from users.api.service import UserService
from tests.factory import UserFactory


def test_get_all_users(user_service: UserService) -> None:
    users = UserFactory.create_batch(5)
    result = user_service.get_all_users()
    assert result == users

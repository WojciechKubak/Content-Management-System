from users.persistance.entity import User
from tests.factory import UserFactory


def test_update() -> None:
    user = UserFactory()

    user.username = f'{user.username}_updated'
    user.update()

    assert User.query.filter_by(id=user.id).first() == user

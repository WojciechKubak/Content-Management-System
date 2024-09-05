from users.persistance.entity import User
from tests.factory import UserFactory


def test_add() -> None:
    user = UserFactory()
    user.add()
    assert User.query.filter_by(id=user.id).first()

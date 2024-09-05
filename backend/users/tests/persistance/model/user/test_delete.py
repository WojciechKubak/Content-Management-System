from users.persistance.entity import User
from tests.factory import UserFactory


def test_delete() -> None:
    user = UserFactory()
    user.delete()
    assert not User.query.filter_by(id=user.id).first()


from users.persistance.entity import Comment, User


def test_set_active(user_model: User) -> None:
    user_model.set_active()
    assert User.query.filter_by(id=user_model.id).first().is_active

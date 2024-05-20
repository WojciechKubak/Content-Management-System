
from users.persistance.entity import Comment, User


def test_user_model_to_json(user_model: User) -> None:
    result = user_model.to_dict()
    assert user_model.__dict__.items() > result.items()

from users.persistance.entity import Comment, User
from typing import Any


def test_comment_model_from_json(comment_dto: dict[str, Any]) -> None:
    comment = Comment.from_dict(comment_dto)
    assert comment_dto.items() < comment.__dict__.items()

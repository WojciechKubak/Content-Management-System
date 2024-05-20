from users.service.comment import CommentService
from users.persistance.entity import Comment, User
from typing import Any
import pytest


class TestCommentServiceAddComment:

    def test_when_user_not_found(self, comment_service: CommentService, comment_dto: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            comment_service.add_comment(comment_dto | {'user_id': 1111})
        assert 'User not found' == str(e.value)

    def test_when_added_succesfully(self, comment_service: CommentService, comment_dto: dict[str, Any]) -> None:
        result = comment_service.add_comment(comment_dto)
        assert Comment.query.filter_by(id=result.id)

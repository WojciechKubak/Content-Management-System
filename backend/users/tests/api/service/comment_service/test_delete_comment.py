from users.api.service import CommentService
from users.persistance.entity import Comment
from tests.factory import CommentFactory, UserFactory
from users.api.exceptions import CommentNotFoundException
import pytest


class TestDeleteComment:

    def test_when_not_found(self, comment_service: CommentService) -> None:
        with pytest.raises(CommentNotFoundException) as e:
            comment_service.delete_comment(999)
        assert CommentNotFoundException().message == str(e.value)

    def test_when_deleted(self, comment_service: CommentService) -> None:
        user = UserFactory()
        comment = CommentFactory(user_id=user.id)

        comment_service.delete_comment(comment.id)

        assert not Comment.query.filter_by(id=comment.id).first()

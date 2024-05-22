from users.api.service import CommentService
from tests.factory import CommentFactory, UserFactory
from users.api.exceptions import CommentNotFoundException
import pytest


class TestCommentServiceGetCommentById:

    def test_when_not_found(self, comment_service: CommentService) -> None:
        with pytest.raises(CommentNotFoundException) as e:
            comment_service.get_comment_by_id(999)
        assert CommentNotFoundException().message == str(e.value)

    def test_when_found(self, comment_service: CommentService) -> None:
        user = UserFactory()
        comment = CommentFactory(user_id=user.id)

        result = comment_service.get_comment_by_id(comment.id)

        assert comment == result

from users.api.service import CommentService
from users.persistance.entity import Comment
from users.api.exceptions import CommentNotFoundException, NotCommentOwnerException
from tests.factory import CommentFactory, UserFactory, CommentDtoFactory
import pytest


class TestUpdateCommentContent:

    def test_when_no_comment(self, comment_service: CommentService) -> None:
        comment_dto = CommentDtoFactory()

        with pytest.raises(CommentNotFoundException) as e:
            comment_service.update_comment_content(comment_dto)

        assert CommentNotFoundException().message in str(e.value)

    def test_when_no_user(self, comment_service: CommentService) -> None:
        user = UserFactory()
        comment = CommentFactory(user_id=user.id)
        comment_dto = CommentDtoFactory(id_=comment.id, user_id=999)

        with pytest.raises(NotCommentOwnerException) as e:
            comment_service.update_comment_content(comment_dto)

        assert NotCommentOwnerException().message in str(e.value)

    def test_when_updated(self, comment_service: CommentService) -> None:
        user = UserFactory()
        comment = CommentFactory(user_id=user.id)
        comment_dto = CommentDtoFactory(
            id_=comment.id,
            user_id=user.id,
            content=f'new_{comment.content}')

        comment_service.update_comment_content(comment_dto)

        assert comment == Comment.query.filter_by(id=comment.id).first()

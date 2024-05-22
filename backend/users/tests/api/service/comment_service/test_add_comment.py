from users.api.service import CommentService
from users.persistance.entity import User
from tests.factory import UserFactory, CommentDtoFactory
from users.api.exceptions import UserNotFoundException
import pytest


class TestAddComment:

    def test_when_user_not_found(self, comment_service: CommentService) -> None:
        comment_dto = CommentDtoFactory()

        with pytest.raises(UserNotFoundException) as e:
            comment_service.add_comment(comment_dto)

        assert UserNotFoundException().message == str(e.value)

    def test_when_added(self, comment_service: CommentService) -> None:
        user = UserFactory()
        comment_dto = CommentDtoFactory(user_id=user.id)
        
        comment_service.add_comment(comment_dto)

        assert User.query.filter_by(id=comment_dto['user_id']).first()

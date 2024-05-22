from users.persistance.entity import Comment
from tests.factory import CommentFactory, UserFactory


def test_find_by_id() -> None:
    user = UserFactory()
    comment = CommentFactory(user_id=user.id)

    result = Comment.find_by_id(comment.id)
    
    assert result == comment

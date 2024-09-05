from users.persistance.entity import Comment
from tests.factory import CommentFactory, UserFactory


def test_add() -> None:
    user = UserFactory()
    comment = CommentFactory(user_id=user.id)

    comment.add()
    
    assert Comment.query.filter_by(id=comment.id).first()

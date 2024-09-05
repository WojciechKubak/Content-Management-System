from users.persistance.entity import Comment
from tests.factory import CommentFactory, UserFactory


def test_delete() -> None:
    user = UserFactory()
    comment = CommentFactory(user_id=user.id)

    comment.delete()
    
    assert not Comment.query.filter_by(id=comment.id).first()

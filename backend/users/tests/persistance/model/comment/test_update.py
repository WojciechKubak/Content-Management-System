from users.persistance.entity import Comment
from tests.factory import CommentFactory, UserFactory


def test_update() -> None:
    user = UserFactory()
    comment = CommentFactory(user_id=user.id)

    comment.content = f'{comment.content}_updated'
    comment.update()

    assert Comment.query.filter_by(id=comment.id).first() == comment

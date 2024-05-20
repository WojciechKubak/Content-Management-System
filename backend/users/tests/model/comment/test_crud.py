from users.persistance.entity import Comment, User
from users.persistance.configuration import sa
from typing import Any, Callable


class TestCommentCrud:

    def test_add(self, comment_model_with_id: Callable[[int], Comment]) -> None:
        new_id = 9999
        comment_with_new_id = comment_model_with_id(new_id)
        comment_with_new_id.add()
        assert sa.session.query(Comment).filter_by(id=new_id).first()

    def test_update(self, comment_model_data: dict[str, Any]) -> None:
        new_content = 'dummy content'
        comment_with_existing_id = Comment(**comment_model_data | {'content': new_content})
        comment_with_existing_id.update()
        expected = sa.session.query(Comment).filter_by(id=comment_model_data['id']).first().content
        assert new_content == expected

    def test_delete(self, comment_model: Comment) -> None:
        id_to_delete = comment_model.id
        comment_model.delete()
        assert not sa.session.query(Comment).filter_by(id=id_to_delete).first()

    def test_find_by_id(self, comment_model: Comment) -> None:
        assert comment_model == Comment.find_by_id(comment_model.id)

from users.api.service import CommentNotFoundException, NotCommentOwnerException
from tests.factory import UserFactory, CommentFactory, CommentDtoFactory
from flask.testing import Client
from flask import url_for


class TestUpdateCommentContent:

    def test_when_comment_not_found(self, client: Client) -> None:
        comment_dto = CommentDtoFactory()

        response = client.put(
            url_for('users.comments.update_comment_content', id_=999), json=comment_dto)

        assert 400 == response.status_code
        assert {'message': CommentNotFoundException().message} == response.json

    def test_when_not_comment_owner(self, client: Client) -> None:
        user = UserFactory()
        comment = CommentFactory(user_id=user.id)
        comment_dto = CommentDtoFactory(user_id=999)

        response = client.put(
            url_for('users.comments.update_comment_content', id_=comment.id), json=comment_dto)

        assert 400 == response.status_code
        assert {'message': NotCommentOwnerException().message} == response.json

    def test_when_updated(self, client: Client) -> None:
        user = UserFactory()
        comment = CommentFactory(user_id=user.id)
        comment_dto = CommentDtoFactory(user_id=user.id)

        response = client.put(
            url_for('users.comments.update_comment_content', id_=comment.id), json=comment_dto)

        assert 200 == response.status_code
        assert comment.id == response.json['id']
        assert comment_dto['content'] == response.json['content']

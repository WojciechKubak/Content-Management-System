from users.api.service import CommentNotFoundException
from tests.factory import CommentFactory, UserFactory
from flask.testing import Client
from flask import url_for


class TestGetCommentById:

    def test_when_comment_not_found(self, client: Client) -> None:
        response = client.delete(url_for('users.comments.get_comment_by_id', id_=999))
        assert 400 == response.status_code
        assert {'message': CommentNotFoundException().message} == response.json

    def test_when_comment_found(self, client: Client) -> None:
        user = UserFactory()
        comment = CommentFactory(user_id=user.id)

        response = client.get(url_for('users.comments.get_comment_by_id', id_=comment.id))

        assert 200 == response.status_code
        assert comment.id == response.json['id']

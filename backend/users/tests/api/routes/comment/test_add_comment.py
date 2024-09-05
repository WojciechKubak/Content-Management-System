from users.api.service import UserNotFoundException
from tests.factory import UserFactory, CommentDtoFactory
from flask.testing import Client
from flask import url_for


class TestAddComment:

    def test_when_user_not_found(self, client: Client) -> None:
        comment_dto = CommentDtoFactory()

        response = client.post(url_for('users.comments.add_comment'), json=comment_dto)

        assert 400 == response.status_code
        assert {'message': UserNotFoundException().message} == response.json

    def test_when_added(self, client: Client) -> None:
        user = UserFactory()
        comment_dto = CommentDtoFactory(user_id=user.id)

        response = client.post(url_for('users.comments.add_comment'), json=comment_dto)

        assert 201 == response.status_code
        assert user.id == response.json['user_id']
        assert comment_dto['content'] == response.json['content']

from tests.factory import CommentFactory, UserFactory
from flask.testing import Client
from flask import url_for


def test_get_user_comments(client: Client) -> None:
    user = UserFactory()
    comments = CommentFactory.create_batch(5, user_id=user.id)

    response = client.get(url_for('users.comments.get_user_comments', id_=user.id))

    assert 200 == response.status_code
    assert len(comments) == len(response.json)

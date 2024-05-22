from tests.factory import CommentFactory, UserFactory
from flask.testing import Client
from flask import url_for


def test_get_article_comments(client: Client) -> None:
    article_id = 1
    user = UserFactory()
    comments = CommentFactory.create_batch(5, article_id=article_id, user_id=user.id)

    response = client.get(url_for('users.comments.get_article_comments', id_=article_id))

    assert 200 == response.status_code
    assert len(comments) == len(response.json)

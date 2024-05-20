
from users.persistance.entity import Comment, User
from flask.testing import Client


def test_user_list_resource_get(client: Client) -> None:
    response = client.get('/users/')
    assert 200 == response.status_code
    assert len(User.query.all()) == len(response.json)

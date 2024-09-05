from tests.factory import UserFactory
from flask.testing import Client
from flask import url_for


def test_get_all_users(client: Client) -> None:
    users = UserFactory.create_batch(5)

    response = client.get(url_for('users.get_all_users'))

    assert 200 == response.status_code
    assert len(users) == len(response.json)

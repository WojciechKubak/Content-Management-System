from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_refresh_token
from unittest.mock import patch


@patch('gateway.security.configure_security.get_jwt_identity')
def test_refresh(mock_get_jwt_identity, client: FlaskClient, app: Flask) -> None:
    mock_get_jwt_identity.return_value = 1

    with app.app_context():
        client.set_cookie('refresh_token_cookie', create_refresh_token(identity=1))
        response = client.post('/refresh')

    assert 200 == response.status_code
    assert 'access_token' in response.json

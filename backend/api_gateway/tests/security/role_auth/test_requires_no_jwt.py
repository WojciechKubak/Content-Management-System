from flask.testing import FlaskClient
from unittest.mock import patch


class TestRequiresNoJWT:

    def test_with_jwt(self, client: FlaskClient) -> None:
        client.set_cookie('access_token_cookie', 'access_token')

        response = client.get('/exposed')
        assert 200 == response.status_code

    @patch('gateway.security.role_auth.verify_jwt_in_request')
    def test_without_jwt(self, mock_verify_jwt, client: FlaskClient) -> None:
        mock_verify_jwt.return_value = None, None
        response = client.get('/exposed')

        assert 403 == response.status_code
        assert b'You are already authenticated' in response.data

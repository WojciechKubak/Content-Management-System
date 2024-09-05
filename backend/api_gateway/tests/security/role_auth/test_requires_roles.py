from flask.testing import FlaskClient
from unittest.mock import patch


class TestRequiresRoles:

    def test_token_missing(self, client: FlaskClient) -> None:
        response = client.get('/protected')
        assert 401 == response.status_code
        assert b'Token is missing or invalid' in response.data

    @patch('gateway.security.role_auth.auth_service.identify_user')
    @patch('gateway.security.role_auth.verify_jwt_in_request')
    def test_not_authorized(self, mock_verify, mock_identify_user, client: FlaskClient) -> None:
        mock_verify.return_value = None, {'sub': 1}
        mock_identify_user.return_value = {'role': 'user'}

        response = client.get('/protected')

        assert 403 == response.status_code
        assert b'Insufficient permissions' in response.data

    @patch('gateway.security.role_auth.auth_service.identify_user')
    @patch('gateway.security.role_auth.verify_jwt_in_request')
    def test_authorized(self, mock_verify, mock_identify_user, client: FlaskClient) -> None:
        mock_verify.return_value = None, {'sub': 1}
        mock_identify_user.return_value = {'role': 'admin'}

        response = client.get('/protected')

        assert 200 == response.status_code
        assert b'Resource accessed successfully' in response.data

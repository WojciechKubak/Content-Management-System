from flask.testing import FlaskClient
from unittest.mock import patch


class TestLogin:

    def test_login_no_credentials(self, client: FlaskClient) -> None:
        response = client.post('/login', json={})
        
        assert 400 == response.status_code
        assert b'No credentials provided' in response.data

    @patch('gateway.security.configure_security.auth_service.verify_user_credentials')
    def test_login_invalid_credentials(self, mock_verify, client: FlaskClient) -> None:
        mock_verify.return_value = None
        
        response = client.post('/login', json={'username': 'user', 'password': '1234'})
        
        assert 401 == response.status_code
        assert b'Invalid credentials' in response.data
    
    @patch('gateway.security.configure_security.auth_service.verify_user_credentials')
    def test_login_success(self, mock_verify, client: FlaskClient) -> None:
        mock_verify.return_value = {'id': 1, 'username': 'user'}
        
        response = client.post('/login', json={'username': 'user', 'password': '1234'})
        
        assert 200 == response.status_code
        assert b'Login successful' in response.data
        assert 'access_token_cookie' in response.headers['Set-Cookie']

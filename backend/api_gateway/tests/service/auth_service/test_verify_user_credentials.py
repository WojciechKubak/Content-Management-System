from gateway.service.auth import AuthService
from unittest.mock import patch
import pytest


class TestVerifyUserCredentials:
    auth_service = AuthService({'USERS_URL': 'http://users-service-url'})

    @patch('httpx.post')
    def test_verification_failure(self, mock_post) -> None:
        mock_post.return_value.status_code = 404
        
        with pytest.raises(ConnectionError) as e:
            self.auth_service.verify_user_credentials('username', 'password')
        
        assert 'Users service - invalid response code' == str(e.value)

    @patch('httpx.post')
    def test_verification_success(self, mock_post) -> None:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'ok'}
        
        result = self.auth_service.verify_user_credentials('username', 'password')
        
        assert {'message': 'ok'} == result

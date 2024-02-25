from gateway.service.auth import AuthService
from unittest.mock import patch
import pytest


class TestIdentifyUser:
    user_service_path = 'http://users-service-url'
    auth_service = AuthService({'USERS_URL': user_service_path})

    @patch('httpx.get')
    def test_identify_user_failure(self, mock_get) -> None:
        mock_get.return_value.status_code = 404
        
        with pytest.raises(ConnectionError) as e:
            self.auth_service.identify_user(1)
    
        assert 'Users service - invalid response code' == str(e.value)

    @patch('httpx.get')
    def test_identify_user_success(self, mock_get) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'id': 1, 'username': 'test'}
        
        result = self.auth_service.identify_user(1)
        
        mock_get.assert_called_once_with(f'{self.user_service_path}/users/1')
        assert {'id': 1, 'username': 'test'} == result

from gateway.service.user import UserService
from unittest.mock import patch
import pytest


class TestProcessRequest:
    user_service = UserService('http://users-service-url')

    @pytest.mark.parametrize('method', ['GET', 'POST', 'PUT', 'DELETE'])
    def test_process_request_failure(self, method: str) -> None:
        with patch('httpx.request') as mock_request:
            mock_request.return_value.status_code = 500

            with pytest.raises(ConnectionError) as e:
                self.user_service.process_request(method, 'resource-path', {'key': 'value'})
            
            assert 'Users service - invalid response code' == str(e.value)

    @pytest.mark.parametrize('method, status_code', [
        ('GET', 200),
        ('POST', 201),
        ('PUT', 200),
        ('DELETE', 204)
    ])
    @patch('httpx.request')
    def test_process_request_success(self, mock_request, method: str, status_code: int) -> None:
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {'message': 'ok'}
        
        result = self.user_service.process_request(method, 'resource-path', {'key': 'value'})
        
        assert {'message': 'ok'}, status_code == result

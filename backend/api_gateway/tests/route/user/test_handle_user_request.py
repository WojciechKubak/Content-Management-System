from gateway.route.user import handle_user_request
from unittest.mock import patch
from flask.testing import FlaskClient

class TestHandleUserRequest:

    @patch('gateway.route.user.user_service.process_request')
    def test_handle_request_failure(self, mock_process_request, app: FlaskClient) -> None:
        mock_process_request.side_effect = ConnectionError('Failed to process request')
        
        with app.app_context():
            response = handle_user_request('GET', 'endpoint', {'key': 'value'})
        
        assert 500 == response.status_code
        assert b'Failed to process request' in response.data

    @patch('gateway.route.user.user_service.process_request')
    def test_handle_request_success(self, mock_process_request, app: FlaskClient) -> None:
        mock_process_request.return_value = ({'message': 'ok'}, 200)
        
        with app.app_context():
            response = handle_user_request('GET', 'endpoint', {'key': 'value'})

        assert 200 == response.status_code
        assert {'message': 'ok'} == response.get_json()

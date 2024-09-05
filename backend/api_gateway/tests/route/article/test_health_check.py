from flask.testing import FlaskClient
from unittest.mock import patch


class TestHealthCheck:

    @patch('gateway.route.article.article_service.check_health')
    def test_check_health_failure(self, mock_check_health, client: FlaskClient) -> None:
        mock_check_health.side_effect = ConnectionError('Articles service - invalid response code')

        response = client.get('/api/articles/health')
        assert 500 == response.status_code
        assert b'Articles service - invalid response code' in response.data

    @patch('gateway.route.article.article_service.check_health')
    def test_check_health_success(self, mock_check_health, client: FlaskClient) -> None:
        mock_check_health.return_value.status_code = 200

        response = client.get('/api/articles/health')

        assert 200 == response.status_code
        assert b'Articles service is working' in response.data

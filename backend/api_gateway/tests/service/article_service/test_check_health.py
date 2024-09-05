from gateway.service.article import ArticleService
from unittest.mock import patch
import pytest


class TestCheckHealth:
    article_service = ArticleService('http://articles-service-url')

    @patch('httpx.get')
    def test_check_health_failure(self, mock_get) -> None:
        mock_get.return_value.status_code = 500

        with pytest.raises(ConnectionError) as e:
            self.article_service.check_health()
        
        assert 'Articles service - invalid response code' == str(e.value)

    @patch('httpx.get')
    def test_check_health_success(self, mock_get) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'status': 'ok'}

        result = self.article_service.check_health()

        assert {'status': 'ok'} == result

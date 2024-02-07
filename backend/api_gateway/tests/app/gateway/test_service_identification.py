from flask.testing import FlaskClient
from unittest.mock import patch
import httpx
import pytest


@pytest.fixture(scope='session')
def mock_request() -> httpx.request:
    with patch('httpx.request') as mock:
        mock_response = httpx.Response(200, content=b'Hello, World!')
        mock.return_value = mock_response
        yield mock


@patch('gateway.app.services', {'test_service': {'url': 'http://test_service_url'}})
def test_gateway_valid_service(client: FlaskClient, mock_request: httpx.request) -> None:
    response = client.get('/api/test_service/test_path')
    assert 200 == response.status_code
    assert b'Hello, World!' == response.data


def test_gateway_invalid_service(client: FlaskClient) -> None:
    response = client.get('/api/invalid_service/some_path')
    assert 400 == response.status_code
    assert b'Invalid service' in response.data

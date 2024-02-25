from unittest.mock import patch
from typing import Generator
import pytest


@pytest.fixture(autouse=True)
def mock_jwt_verification() -> Generator:
    with patch('gateway.security.role_auth.verify_jwt_in_request') as mock_verify_jwt, \
         patch('gateway.security.role_auth.auth_service.identify_user') as mock_identify_user:

        mock_verify_jwt.return_value = (None, {'sub': 'test_user'})
        mock_identify_user.return_value = {'role': 'admin'}

        yield

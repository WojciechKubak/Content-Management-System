from dataclasses import dataclass
from typing import Any
import httpx


@dataclass
class AuthService:
    """
    A service for interacting with the users API.

    Attributes:
        users_url (str): The base URL of the users API.
    """
    users_url: str

    def verify_user_credentials(self, username: str, password: str) -> dict[str, Any]:
        """
        Verifies a user's credentials.

        Args:
            username (str): The username to verify.
            password (str): The password to verify.

        Returns:
            dict[str, Any]: The JSON response from the users API.

        Raises:
            ConnectionError: If the response status code is not in the 200 range.
        """
        url = f'{self.users_url}/users/credentials'
        data = {
            'username': username,
            'password': password
        }
        response = httpx.post(url, json=data)
        if not str(response.status_code).startswith('2'):
            raise ConnectionError('Users service - invalid response code')
        return response.json()
    
    def identify_user(self, user_id: int) -> dict[str, Any]:
        """
        Identifies a user.

        Args:
            user_id (int): The ID of the user to identify.

        Returns:
            dict[str, Any]: The JSON response from the users API.

        Raises:
            ConnectionError: If the response status code is not in the 200 range.
        """
        url = f'{self.users_url}/users/{user_id}'
        response = httpx.get(url)
        if not str(response.status_code).startswith('2'):
            raise ConnectionError('Users service - invalid response code')
        return response.json()

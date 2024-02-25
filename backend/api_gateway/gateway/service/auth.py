from dataclasses import dataclass
from typing import Any
import httpx


@dataclass
class AuthService:
    config: dict[str, Any]

    def verify_user_credentials(self, username: str, password: str) -> dict[str, Any]:
        url = self.config['USERS_URL'] + '/users/credentials'
        data = {
            'username': username,
            'password': password
        }
        response = httpx.post(url, json=data)
        if not str(response.status_code).startswith('2'):
            raise ConnectionError('Users service - invalid response code')
        return response.json()
    
    def identify_user(self, user_id: int) -> dict[str, Any]:
        url = self.config['USERS_URL'] + f'/users/{user_id}'
        response = httpx.get(url)
        if not str(response.status_code).startswith('2'):
            raise ConnectionError('Users service - invalid response code')
        return response.json()

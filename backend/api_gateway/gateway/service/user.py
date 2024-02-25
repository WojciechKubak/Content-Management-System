from dataclasses import dataclass
from typing import Any
import httpx


@dataclass
class UserService:
    users_url: str

    def check_health(self) -> dict[str, Any]:
        response = httpx.get(f'{self.users_url}/health')
        if not str(response.status_code).startswith('2'):
            raise ConnectionError('Users service - invalid response code')
        return response.json()
    
    def process_request(self, method: str, path: str, data: dict[str, Any]) -> tuple[dict[str, Any], int]:
        response = httpx.request(method.upper(), f'{self.users_url}/{path}', json=data)
        if str(response.status_code).startswith('5'):
            raise ConnectionError('Users service - invalid response code')
        return response.json(), response.status_code

from dataclasses import dataclass
from typing import Any
import httpx


@dataclass
class ArticleService:
    """
    A service for interacting with the articles API.

    Attributes:
        articles_url (str): The base URL of the articles API.
    """
    articles_url: str

    def check_health(self) -> dict[str, Any]:
        """
        Checks the health of the articles API.

        Returns:
            dict[str, Any]: The JSON response from the health check endpoint.

        Raises:
            ConnectionError: If the response status code is not in the 200 range.
        """
        response = httpx.get(f'{self.articles_url}/health')
        if not str(response.status_code).startswith('2'):
            raise ConnectionError('Articles service - invalid response code')
        return response.json()
    
    def process_request(self, method: str, path: str, data: dict[str, Any]) -> tuple[dict[str, Any], int]:
        """
        Processes a request to the articles API.

        Args:
            method (str): The HTTP method to use.
            path (str): The path of the endpoint to hit.
            data (dict[str, Any]): The data to send with the request.

        Returns:
            tuple[dict[str, Any], int]: The JSON response and the status code from the request.

        Raises:
            ConnectionError: If the response status code is in the 500 range.
        """        
        response = httpx.request(method.upper(), f'{self.articles_url}/{path}', json=data)
        if str(response.status_code).startswith('5'):
            raise ConnectionError('Articles service - invalid response code')
        return response.json(), response.status_code

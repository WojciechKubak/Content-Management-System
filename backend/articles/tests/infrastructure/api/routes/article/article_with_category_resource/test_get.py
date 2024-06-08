from flask.testing import Client
from flask import url_for
from unittest.mock import MagicMock, patch


def test_get_articles_with_category(client: Client, base_path: str) -> None:
    mock_article = MagicMock()
    mock_article.to_dict.return_value = {"id": 1, "title": "test_title"}

    with patch(
        f"{base_path}.article_service.get_articles_with_category"
    ) as mock_get_articles:
        mock_get_articles.return_value = [mock_article]
        response = client.get(url_for("articleswithcategoryresource", category_id=1))

    mock_get_articles.assert_called_once()
    assert 200 == response.status_code
    assert [{"id": 1, "title": "test_title"}] == response.get_json()

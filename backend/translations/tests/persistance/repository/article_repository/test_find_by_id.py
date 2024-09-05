from tests.factory import ArticleFactory
from translations.persistance.repository import ArticleRepository


def test_find_by_id(article_repository: ArticleRepository) -> None:
    article = ArticleFactory()
    result = article_repository.find_by_id(article.id)
    assert article == result

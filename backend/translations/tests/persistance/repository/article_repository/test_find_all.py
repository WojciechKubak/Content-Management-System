from tests.factory import ArticleFactory
from translations.persistance.repository import ArticleRepository


def test_find_all(article_repository: ArticleRepository) -> None:
    articles = ArticleFactory.create_batch(5)
    result = article_repository.find_all()
    assert articles == result

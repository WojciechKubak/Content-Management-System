from tests.factory import ArticleFactory
from translations.persistance.repository import ArticleRepository
from translations.persistance.entity import Article
from translations.persistance.configuration import sa


def test_delete_by_id(article_repository: ArticleRepository) -> None:
    article = ArticleFactory()
    article_repository.delete_by_id(article.id)
    assert not sa.session.query(Article).filter_by(id=article.id).first()

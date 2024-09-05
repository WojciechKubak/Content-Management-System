from tests.factory import ArticleFactory
from translations.persistance.repository import ArticleRepository
from translations.persistance.entity import Article
from translations.persistance.configuration import sa


class TestSaveOrUpdate:

    def test_when_saved(self, article_repository: ArticleRepository) -> None:
        article = ArticleFactory.build()
        result = article_repository.save_or_update(article)
        assert sa.session.query(Article).filter_by(id=result.id).first()

    def test_when_updated(self, article_repository: ArticleRepository) -> None:
        article = ArticleFactory()
        updated_title = f"updated {article.title}"
        article.title = updated_title

        article_repository.save_or_update(article)

        assert sa.session.query(Article).filter_by(id=article.id).first().title == updated_title

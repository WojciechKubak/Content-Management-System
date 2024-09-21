from translations.db.entities import Language, Article, Translation
from translations.common.models import SimpleModel
from translations.db.configuration import sa
from factory import Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker


fake = Faker()


class SimpleModelFactory(SQLAlchemyModelFactory):
    class Meta:
        model = SimpleModel
        sqlalchemy_session = sa.session

    id = Sequence(lambda n: n + 1)
    name = fake.name()


class LanguageFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Language
        sqlalchemy_session = sa.session

    id = Sequence(lambda n: n + 1)

    name = fake.language_name()
    code = fake.language_code()


class ArticleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Article
        sqlalchemy_session = sa.session

    id = Sequence(lambda n: n + 1)

    title = fake.sentence(nb_words=6)
    content_path = fake.file_path(depth=2, category="text")


class TranslationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Translation
        sqlalchemy_session = sa.session

    id = Sequence(lambda n: n + 1)

    article = SubFactory(ArticleFactory)

    title = fake.sentence(nb_words=6)
    content_path = fake.file_path(depth=2, category="text")
    language = SubFactory(LanguageFactory)
    requested_at = fake.date_time_this_year()
    status = Translation.StatusType.PENDING

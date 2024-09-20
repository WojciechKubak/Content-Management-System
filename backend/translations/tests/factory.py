from translations.persistance.entity import Language, Article, Translation
from translations.persistance.configuration import sa
from faker import Faker
from factory import Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory


fake = Faker()


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

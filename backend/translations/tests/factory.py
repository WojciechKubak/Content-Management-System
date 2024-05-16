from translations.persistance.entity import Language, Article, Translation, StatusType, sa
from translations.broker.dto import (
    LanguageEventDTO, 
    LanguageEventType, 
    ArticleTranslationRequestDTO,
    ArticleTranslationDTO
)
from factory import Sequence, SubFactory, Factory
from factory.alchemy import SQLAlchemyModelFactory
from datetime import datetime


class LanguageFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Language
        sqlalchemy_session = sa.session

    id = Sequence(lambda n: n + 1)
    name = 'english'
    code = 'EN'


class ArticleFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Article
        sqlalchemy_session = sa.session

    id = Sequence(lambda n: n + 1)
    title = 'Article title'
    content_path = 'subfolder/article_content.txt'


class TranslationFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Translation
        sqlalchemy_session = sa.session

    id = Sequence(lambda n: n + 1)
    article = SubFactory(ArticleFactory)
    title='Translated article title'
    content_path='subfolder/translation_content.txt'
    language = SubFactory(LanguageFactory)
    requested_at = datetime.now()
    status = StatusType.PENDING


class LanguageEventDTOFactory(Factory):
    
    class Meta:
        model = LanguageEventDTO

    id_ = Sequence(lambda n: n + 1)
    name = 'English'
    code = 'EN'
    event_type = LanguageEventType.CREATE


class ArticleTranslationRequestDTOFactory(Factory):

    class Meta:
        model = ArticleTranslationRequestDTO

    id_ = Sequence(lambda n: n + 1)
    title = 'Article title'
    content_path = 'subfolder/article_content.txt'
    language_id = Sequence(lambda n: n + 1)
    date = datetime.now()


class ArticleTranslationDTOFactory(Factory):

    class Meta:
        model = ArticleTranslationDTO

    id_ = Sequence(lambda n: n + 1)
    language_id = Sequence(lambda n: n + 1)
    title = 'Article title'
    content_path = 'subfolder/article_content.txt'
    translator_id = Sequence(lambda n: n + 1)

from tests.factory import LanguageFactory, ArticleFactory, TranslationFactory, ArticleTranslationRequestDTOFactory
from translations.broker.consumer import EventConsumerService
from translations.api.exceptions import EntityNotFoundError, EntityAlreadyExistsError
from translations.persistance.entity import Article, Translation
from translations.persistance.configuration import sa
import pytest


class TestHandleTranslationRequest:

    def test_when_no_language(self, event_consumer_service: EventConsumerService) -> None:
        dto = ArticleTranslationRequestDTOFactory()

        with pytest.raises(EntityNotFoundError) as e:
            event_consumer_service.handle_translation_request(dto)

        assert EntityNotFoundError('Language not found').message == str(e.value)

    def test_when_translation_exists(self, event_consumer_service: EventConsumerService) -> None:
        translation = TranslationFactory.create()
        sa.session.commit()
        dto = ArticleTranslationRequestDTOFactory(
            id_=translation.article_id,
            language_id=translation.language_id,
        )

        with pytest.raises(EntityAlreadyExistsError) as e:
            event_consumer_service.handle_translation_request(dto)

        assert EntityAlreadyExistsError('Translation already exists').message == str(e.value)

    def test_when_no_article(self, event_consumer_service: EventConsumerService) -> None:
        language = LanguageFactory()
        dto = ArticleTranslationRequestDTOFactory(language_id=language.id)

        event_consumer_service.handle_translation_request(dto)

        assert sa.session.query(Article).filter_by(id=dto.id_).first()
        assert sa.session.query(Translation).filter_by(article_id=dto.id_).first()

        
    def test_when_article_exists(self, event_consumer_service: EventConsumerService) -> None:
        ArticleFactory()
        language = LanguageFactory()
        dto = ArticleTranslationRequestDTOFactory(language_id=language.id)     

        event_consumer_service.handle_translation_request(dto)

        assert sa.session.query(Translation).filter_by(article_id=dto.id_).first()

from translations.persistance.repository import (
    LanguageRepository,
    TranslationRepository,
    ArticleRepository,
)
from translations.broker.consumer import EventConsumerService
import pytest


@pytest.fixture(scope="session")
def event_consumer_service(
    language_repository: LanguageRepository,
    translation_repository: TranslationRepository,
    article_repository: ArticleRepository,
) -> EventConsumerService:
    return EventConsumerService(
        language_repository=language_repository,
        translation_repository=translation_repository,
        article_repository=article_repository,
    )

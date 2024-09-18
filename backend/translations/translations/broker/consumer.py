from translations.broker.dto import ArticleTranslationRequestDTO
from translations.persistance.repository import (
    LanguageRepository,
    TranslationRepository,
    ArticleRepository,
)
from translations.api.exceptions import EntityNotFoundError, EntityAlreadyExistsError
from dataclasses import dataclass


@dataclass
class EventConsumerService:
    language_repository: LanguageRepository
    translation_repository: TranslationRepository
    article_repository: ArticleRepository

    def handle_translation_request(
        self, article_translation_request_dto: ArticleTranslationRequestDTO
    ) -> None:
        if not self.language_repository.find_by_id(
            article_translation_request_dto.language_id
        ):
            raise EntityNotFoundError("Language not found")
        if self.translation_repository.find_by_language_and_article(
            article_translation_request_dto.language_id,
            article_translation_request_dto.id_,
        ):
            raise EntityAlreadyExistsError("Translation already exists")

        article = self.article_repository.find_by_id(
            article_translation_request_dto.id_
        )
        if not article:
            article = self.article_repository.save_or_update(
                article_translation_request_dto.to_article_entity()
            )

        self.translation_repository.save_or_update(
            article_translation_request_dto.to_translation_entity()
        )

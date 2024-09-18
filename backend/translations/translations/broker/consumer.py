from translations.broker.dto import (
    ArticleTranslationRequestDTO,
    LanguageEventDTO,
    LanguageEventType,
)
from translations.persistance.repository import (
    LanguageRepository,
    TranslationRepository,
    ArticleRepository,
)
from translations.api.exceptions import (
    EntityNotFoundError,
    EntityAlreadyExistsError,
    InvalidStatusOperationError,
)
from translations.storage.boto3 import Boto3Service
from dataclasses import dataclass


@dataclass
class EventConsumerService:
    """
    A service class that handles translation requests and language events.

    Attributes:
        language_repository (LanguageRepository): The repository for Language entities.
        translation_repository (TranslationRepository): The repository for Translation entities.
        article_repository (ArticleRepository): The repository for Article entities.
        storage_service (Boto3Service): The service for handling storage operations.
    """

    language_repository: LanguageRepository
    translation_repository: TranslationRepository
    article_repository: ArticleRepository
    storage_service: Boto3Service

    def handle_translation_request(
        self, article_translation_request_dto: ArticleTranslationRequestDTO
    ) -> None:
        """
        Handles a translation request.

        This method checks if the requested language exists and if a translation for the given language and article
        already exists. If the article doesn't exist, it saves or updates the article entity. Finally, it saves or
        updates the translation entity.

        Args:
            article_translation_request_dto (ArticleTranslationRequestDTO): The DTO for the translation request.

        Raises:
            EntityNotFoundError: If the requested language doesn't exist.
            EntityAlreadyExistsError: If a translation for the given language and article already exists.
        """
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

    def handle_language_event(self, language_event_dto: LanguageEventDTO) -> None:
        """
        Handles a language event.

        This method performs different operations depending on the event type of the LanguageEventDTO. For a CREATE
        event, it saves or updates the language entity if it doesn't exist. For an UPDATE event, it saves or updates
        the language entity if it exists. For a DELETE event, it deletes the language entity if it exists.

        Args:
            language_event_dto (LanguageEventDTO): The DTO for the language event.

        Raises:
            EntityNotFoundError: If the language doesn't exist for an UPDATE or DELETE event.
            EntityAlreadyExistsError: If the language already exists for a CREATE event.
            InvalidStatusOperationError: If the event type is not CREATE, UPDATE, or DELETE.
        """
        result = self.language_repository.find_by_id(language_event_dto.id_)
        match language_event_dto.event_type:

            case LanguageEventType.CREATE:
                if result:
                    raise EntityAlreadyExistsError("Language already exists")
                self.language_repository.save_or_update(language_event_dto.to_entity())

            case LanguageEventType.UPDATE:
                if not result:
                    raise EntityNotFoundError("Language not found")
                self.language_repository.save_or_update(language_event_dto.to_entity())

            case LanguageEventType.DELETE:
                if not result:
                    raise EntityNotFoundError("Language not found")
                self.language_repository.delete_by_id(language_event_dto.id_)

            case _:
                raise InvalidStatusOperationError()

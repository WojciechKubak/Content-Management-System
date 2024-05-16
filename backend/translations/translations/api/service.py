from translations.persistance.repository import LanguageRepository, TranslationRepository
from translations.api.dto import TranslationDTO, ListTranslationDTO
from translations.persistance.entity import StatusType
from translations.storage.boto3 import Boto3Service
from translations.broker.kafka import KafkaService
from translations.gpt.chat_gpt import ChatGPTService
from translations.gpt.dto import ChatGptTitleTranslationDTO, ChatGptContentTranslationDTO
from translations.broker.dto import ArticleTranslationDTO
from translations.api.exceptions import (
    EntityNotFoundError,
    MissingDataError,
    InvalidRedactorIdError,
    InvalidStatusOperationError,
    TranslationAlreadyReleasedError,
    TranslationNotPendingError
)
from dataclasses import dataclass


@dataclass
class ApiService:
    """
    A service class for handling translation related operations.

    Attributes:
        language_repository (LanguageRepository): A repository for language related operations.
        translation_repository (TranslationRepository): A repository for translation related operations.
        kafka_service (KafkaService): A service for Kafka related operations.
        storage_service (Boto3Service): A service for storage related operations.
        chat_gpt_service (ChatGPTService): A service for GPT-3 chat related operations.
        translated_articles_topic (str): The topic name for translated articles in Kafka.
        translations_subfolder (str): The subfolder name for translations in storage.
    """

    language_repository: LanguageRepository
    translation_repository: TranslationRepository
    kafka_service: KafkaService
    storage_service: Boto3Service
    chat_gpt_service: ChatGPTService
    translated_articles_topic: str
    translations_subfolder: str

    def get_translation_by_id(self, translation_id: int) -> TranslationDTO:
        """
        Retrieves a translation by its ID.

        Args:
            translation_id (int): The ID of the translation.

        Returns:
            TranslationDTO: The translation data transfer object.

        Raises:
            EntityNotFoundError: If the translation is not found.
        """
        translation = self.translation_repository.find_by_id(translation_id)
        if not translation:
            raise EntityNotFoundError('Translation not found')
        return TranslationDTO \
            .from_entity(translation) \
            .with_contents(
                self.storage_service.read_file_content(translation.article.content_path),
                self.storage_service.read_file_content(translation.content_path)
                if translation.content_path else None
            )

    def get_translations_by_language(self, language_id: int) -> list[ListTranslationDTO]:
        """
        Retrieves all translations for a specific language.

        Args:
            language_id (int): The ID of the language.

        Returns:
            list[ListTranslationDTO]: A list of translation data transfer objects.

        Raises:
            EntityNotFoundError: If the language is not found.
        """
        if not self.language_repository.find_by_id(language_id):
            raise EntityNotFoundError('Language not found')
        result = self.translation_repository.find_by_language(language_id)
        return [ListTranslationDTO.from_entity(translation) for translation in result]

    def get_all_translations(self) -> list[ListTranslationDTO]:
        """
        Retrieves all translations.

        Returns:
            list[ListTranslationDTO]: A list of translation data transfer objects.
        """
        result = self.translation_repository.find_all()
        return [ListTranslationDTO.from_entity(translation) for translation in result]

    def change_translation_content(self, translation_id: int, new_content: str) -> TranslationDTO:
        """
        Changes the content of a translation.

        Args:
            translation_id (int): The ID of the translation.
            new_content (str): The new content for the translation.

        Returns:
            TranslationDTO: The updated translation data transfer object.

        Raises:
            MissingDataError: If the new content is not provided.
            EntityNotFoundError: If the translation is not found.
            TranslationNotPendingError: If the translation is not in pending status.
        """
        if not new_content:
            raise MissingDataError()
        result = self.translation_repository.find_by_id(translation_id)
        if not result:
            raise EntityNotFoundError('Translation not found')
        if result.status != StatusType.PENDING:
            raise TranslationNotPendingError()
        if result.content_path:
            self.storage_service.update_file_content(result.content_path, new_content)
        else:
            result.content_path = self.storage_service.upload_to_txt_file(
                new_content,
                self.translations_subfolder
            )
            self.translation_repository.save_or_update(result)

        return TranslationDTO.from_entity(result) \
            .with_contents(
                self.storage_service.read_file_content(result.article.content_path),
                new_content)
    
    def change_translation_title(self, translation_id: int, new_title: str) -> TranslationDTO:
        """
        Changes the title of a translation.

        Args:
            translation_id (int): The ID of the translation.
            new_title (str): The new title for the translation.

        Returns:
            TranslationDTO: The updated translation data transfer object.

        Raises:
            MissingDataError: If the new title is not provided.
            EntityNotFoundError: If the translation is not found.
            TranslationNotPendingError: If the translation is not in pending status.
        """
        if not new_title:
            raise MissingDataError()
        result = self.translation_repository.find_by_id(translation_id)
        if not result:
            raise EntityNotFoundError('Translation not found')
        if result.status != StatusType.PENDING:
            raise TranslationNotPendingError()
        
        result.title = new_title
        self.translation_repository.save_or_update(result)

        return TranslationDTO.from_entity(result). \
            with_contents(
                self.storage_service.read_file_content(result.article.content_path),
                self.storage_service.read_file_content(result.content_path)
                if result.content_path else None
        )
    
    def change_translation_status(self, translation_id: int, status_type: str, redactor_id: int) -> ListTranslationDTO:
        """
        Changes the status of a translation.

        Args:
            translation_id (int): The ID of the translation.
            status_type (str): The new status for the translation.
            redactor_id (int): The ID of the redactor.

        Returns:
            ListTranslationDTO: The updated translation data transfer object.

        Raises:
            EntityNotFoundError: If the translation is not found.
            InvalidRedactorIdError: If the redactor ID is not valid.
            InvalidStatusOperationError: If the status type is not valid.
            TranslationAlreadyReleasedError: If the translation is already released.
        """
        result = self.translation_repository.find_by_id(translation_id)
        if not result:
            raise EntityNotFoundError('Translation not found')
        if redactor_id <= 0:
            raise InvalidRedactorIdError()
        if status_type.upper() not in StatusType.__members__:
            raise InvalidStatusOperationError()
        if result.status == StatusType.RELEASED:
            raise TranslationAlreadyReleasedError()
        
        match StatusType[status_type.upper()]:

            case StatusType.REQUESTED:
                result.translator_id = None
                result.status = StatusType.REQUESTED

            case StatusType.PENDING:
                result.translator_id = redactor_id
                result.status = StatusType.PENDING

            case StatusType.COMPLETED:
                result.status = StatusType.COMPLETED

            case StatusType.RELEASED:
                result.status = StatusType.RELEASED
                self.kafka_service.produce_message(
                    self.translated_articles_topic,
                    ArticleTranslationDTO.from_entity(result)
                )

            case StatusType.REJECTED:
                result.status = StatusType.REJECTED
                result.translator_id = None
            
        self.translation_repository.save_or_update(result)
        return ListTranslationDTO.from_entity(result)

    def translate_title(self, translation_id: int) -> str:
        """
        Translates the title of a translation.

        Args:
            translation_id (int): The ID of the translation.

        Returns:
            str: The translated title.

        Raises:
            EntityNotFoundError: If the translation is not found.
            TranslationNotPendingError: If the translation is not in pending status.
        """
        result = self.translation_repository.find_by_id(translation_id)
        if not result:
            raise EntityNotFoundError('Translation not found')
        if result.status != StatusType.PENDING:
            raise TranslationNotPendingError()
        return self.chat_gpt_service.get_translation(
            ChatGptTitleTranslationDTO.from_entity(result)
        )

    def translate_content(self, translation_id: int) -> str:
        """
        Translates the content of a translation.

        Args:
            translation_id (int): The ID of the translation.

        Returns:
            str: The translated content.

        Raises:
            EntityNotFoundError: If the translation is not found.
            TranslationNotPendingError: If the translation is not in pending status.
        """
        result = self.translation_repository.find_by_id(translation_id)
        if not result:
            raise EntityNotFoundError('Translation not found')
        if result.status != StatusType.PENDING:
            raise TranslationNotPendingError()
        content = self.storage_service.read_file_content(result.article.content_path)
        return self.chat_gpt_service.get_translation(
            ChatGptContentTranslationDTO.from_entity(result, content)
        )

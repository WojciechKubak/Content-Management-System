from translations.persistance.repository import (
    LanguageRepository,
    TranslationRepository,
)

from translations.config.settings.storages import STORAGE_TYPE_STRATEGY
from backend.translations.translations.enums.enums import StorageType
from translations.integrations.aws.client import text_to_file_upload, file_get_content
from translations.common.services import (
    text_to_local_file_upload,
    file_get_local_content,
)

from translations.config.settings.translations import TRANSLATION_TYPE_STRATEGY
from backend.translations.translations.enums.enums import TranslationType
from translations.common.services import content_get_local_translation
from translations.integrations.gpt.client import (
    BaseTranslationRequest,
    TitleTranslationRequest,
    ContentTranslationRequest,
    content_get_translation,
)


from translations.api.dto import TranslationDTO, ListTranslationDTO
from translations.persistance.entity import StatusType
from translations.broker.kafka import KafkaService

from translations.broker.dto import ArticleTranslationDTO
from translations.api.exceptions import (
    EntityNotFoundError,
    MissingDataError,
    InvalidRedactorIdError,
    # InvalidStatusOperationError,
    TranslationAlreadyReleasedError,
    TranslationNotPendingError,
)
from dataclasses import dataclass


def get_content(*, file_name: str) -> str:
    if STORAGE_TYPE_STRATEGY == StorageType.LOCAL:
        return file_get_local_content(file_name=file_name)
    else:
        return file_get_content(file_name=file_name)


def file_upload(*, file_name: str, content: str) -> str:
    if STORAGE_TYPE_STRATEGY == STORAGE_TYPE_STRATEGY.LOCAL:
        return text_to_local_file_upload(file_name=file_name, content=content)
    else:
        return text_to_file_upload(file_name=file_name, content=content)


def get_translation(*, request: type[BaseTranslationRequest]) -> str:
    if TRANSLATION_TYPE_STRATEGY == TranslationType.LOCAL:
        return content_get_local_translation(request.content, request.language)
    else:
        return content_get_translation(request=request)


@dataclass
class ApiService:
    language_repository: LanguageRepository
    translation_repository: TranslationRepository
    kafka_service: KafkaService
    translated_articles_topic: str
    translations_subfolder: str

    def get_translation_by_id(self, translation_id: int) -> TranslationDTO:
        translation = self.translation_repository.find_by_id(translation_id)
        if not translation:
            raise EntityNotFoundError("Translation not found")

        original = get_content(file_name=translation.article.content_path)
        translated = (
            get_content(file_name=translation.content_path)
            if translation.content_path
            else None
        )

        return TranslationDTO.from_entity(translation).with_contents(
            original, translated
        )

    def get_translations_by_language(
        self, language_id: int
    ) -> list[ListTranslationDTO]:
        if not self.language_repository.find_by_id(language_id):
            raise EntityNotFoundError("Language not found")

        result = self.translation_repository.find_by_language(language_id)

        return [ListTranslationDTO.from_entity(translation) for translation in result]

    def get_all_translations(self) -> list[ListTranslationDTO]:
        result = self.translation_repository.find_all()
        return [ListTranslationDTO.from_entity(translation) for translation in result]

    def change_translation_content(
        self, translation_id: int, new_content: str
    ) -> TranslationDTO:
        if not new_content:
            raise MissingDataError()

        result = self.translation_repository.find_by_id(translation_id)
        if not result:
            raise EntityNotFoundError("Translation not found")

        if result.status != StatusType.PENDING:
            raise TranslationNotPendingError()

        # todo: those conditions might be merged
        if result.content_path:
            file_upload(file_name=result.content_path, content=new_content)

        else:
            result.content_path = file_upload(
                file_name=new_content, content=self.translations_subfolder
            )
            self.translation_repository.save_or_update(result)

        content = get_content(file_name=result.article.content_path)

        return TranslationDTO.from_entity(result).with_contents(content, new_content)

    def change_translation_title(
        self, translation_id: int, new_title: str
    ) -> TranslationDTO:
        if not new_title:
            raise MissingDataError()
        result = self.translation_repository.find_by_id(translation_id)

        if not result:
            raise EntityNotFoundError("Translation not found")

        if result.status != StatusType.PENDING:
            raise TranslationNotPendingError()

        result.title = new_title
        self.translation_repository.save_or_update(result)

        # todo: this might get merged
        return TranslationDTO.from_entity(result).with_contents(
            get_content(file_name=result.article.content_path),
            get_content(file_name=result.content_path) if result.content_path else None,
        )

    def change_translation_status(
        self, translation_id: int, status_type: str, redactor_id: int
    ) -> ListTranslationDTO:
        result = self.translation_repository.find_by_id(translation_id)
        if not result:
            raise EntityNotFoundError("Translation not found")

        if redactor_id <= 0:
            raise InvalidRedactorIdError()

        # todo: add this again
        # if status_type.upper() not in StatusType.__members__:
        #     raise InvalidStatusOperationError()

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
                    ArticleTranslationDTO.from_entity(result),
                )

            case StatusType.REJECTED:
                result.status = StatusType.REJECTED
                result.translator_id = None

        self.translation_repository.save_or_update(result)

        return ListTranslationDTO.from_entity(result)

    def translate_title(self, translation_id: int) -> str:
        result = self.translation_repository.find_by_id(translation_id)

        if not result:
            raise EntityNotFoundError("Translation not found")

        if result.status != StatusType.PENDING:
            raise TranslationNotPendingError()

        return get_translation(
            request=TitleTranslationRequest(result.title, result.language)
        )

    def translate_content(self, translation_id: int) -> str:
        result = self.translation_repository.find_by_id(translation_id)

        if not result:
            raise EntityNotFoundError("Translation not found")

        if result.status != StatusType.PENDING:
            raise TranslationNotPendingError()

        content = get_content(file_name=result.article.content_path)

        return get_translation(
            request=ContentTranslationRequest(content, result.language)
        )

from translations.config.config import TRANSLATED_ARTICLES_TOPIC
from translations.persistance.repository import (
    language_repository,
    translation_repository,
)
from translations.config.config import STORAGE_TYPE_STRATEGY
from translations.enums.enums import StorageType
from translations.integrations.aws.client import text_to_file_upload, file_get_content
from translations.common.services import (
    text_to_local_file_upload,
    file_get_local_content,
    file_name_generate,
)
from translations.config.config import TRANSLATION_TYPE_STRATEGY
from translations.enums.enums import TranslationType
from translations.common.services import content_get_local_translation
from translations.integrations.gpt.client import (
    BaseTranslationRequest,
    TitleTranslationRequest,
    ContentTranslationRequest,
    content_get_translation,
)
from translations.integrations.kafka.producer import (
    TranslationResponse,
    produce_message,
)
from translations.services.dtos import (
    TranslationDTO,
    ListTranslationDTO,
)
from translations.persistance.entity import StatusType
from translations.core.exceptions import ValidationError


TRANSLATION_NOT_FOUND_ERROR_MSG: str = "Translation not found"
LANGUAGE_NOT_FOUND_ERROR_MSG: str = "Language not found"
MISSING_DATA_ERROR_MSG: str = "No data provided"
TRANSLATION_NOT_PENDING_ERROR_MSG: str = "Translation is not pending"
TRANSLATION_ALREADY_RELEASED_ERROR_MSG: str = "Translation is already released"


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


def get_translation_by_id(*, translation_id: int) -> TranslationDTO:
    translation = translation_repository.find_by_id(translation_id)
    if not translation:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    original = get_content(file_name=translation.article.content_path)
    translated = (
        get_content(file_name=translation.content_path)
        if translation.content_path
        else None
    )

    return TranslationDTO.from_entity(translation).with_contents(original, translated)


def get_translations_by_language(*, language_id: int) -> list[ListTranslationDTO]:
    if not language_repository.find_by_id(language_id):
        raise ValidationError(LANGUAGE_NOT_FOUND_ERROR_MSG)

    result = translation_repository.find_by_language(language_id)

    return [ListTranslationDTO.from_entity(translation) for translation in result]


def get_all_translations() -> list[ListTranslationDTO]:
    result = translation_repository.find_all()
    return [ListTranslationDTO.from_entity(translation) for translation in result]


def change_translation_content(
    *, translation_id: int, new_content: str
) -> TranslationDTO:
    if not new_content:
        raise ValidationError(MISSING_DATA_ERROR_MSG)

    result = translation_repository.find_by_id(translation_id)
    if not result:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    if result.status != StatusType.PENDING:
        raise ValidationError(TRANSLATION_NOT_PENDING_ERROR_MSG)

    # todo: those conditions might be merged
    if result.content_path:
        file_upload(file_name=result.content_path, content=new_content)

    else:
        result.content_path = file_upload(
            file_name=file_name_generate(), content=new_content
        )
        translation_repository.save_or_update(result)

    content = get_content(file_name=result.article.content_path)

    return TranslationDTO.from_entity(result).with_contents(content, new_content)


def change_translation_title(*, translation_id: int, new_title: str) -> TranslationDTO:
    if not new_title:
        raise ValidationError(MISSING_DATA_ERROR_MSG)
    result = translation_repository.find_by_id(translation_id)

    if not result:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    if result.status != StatusType.PENDING:
        raise ValidationError(TRANSLATION_NOT_PENDING_ERROR_MSG)

    result.title = new_title
    translation_repository.save_or_update(result)

    # todo: this might get merged
    return TranslationDTO.from_entity(result).with_contents(
        get_content(file_name=result.article.content_path),
        get_content(file_name=result.content_path) if result.content_path else None,
    )


def change_translation_status(
    *, translation_id: int, status_type: str, redactor_id: int
) -> ListTranslationDTO:
    result = translation_repository.find_by_id(translation_id)
    if not result:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    # todo: add this again
    # if status_type.upper() not in StatusType.__members__:
    #     raise InvalidStatusOperationError()

    if result.status == StatusType.RELEASED:
        raise ValidationError(TRANSLATION_ALREADY_RELEASED_ERROR_MSG)

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
            produce_message(
                TRANSLATED_ARTICLES_TOPIC,
                TranslationResponse.from_entity(result),
            )

        case StatusType.REJECTED:
            result.status = StatusType.REJECTED
            result.translator_id = None

    translation_repository.save_or_update(result)

    return ListTranslationDTO.from_entity(result)


def translate_title(*, translation_id: int) -> str:
    result = translation_repository.find_by_id(translation_id)

    if not result:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    if result.status != StatusType.PENDING:
        raise ValidationError(TRANSLATION_NOT_PENDING_ERROR_MSG)

    return get_translation(
        request=TitleTranslationRequest(result.title, result.language)
    )


def translate_content(*, translation_id: int) -> str:
    result = translation_repository.find_by_id(translation_id)

    if not result:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    if result.status != StatusType.PENDING:
        raise ValidationError(TRANSLATION_NOT_PENDING_ERROR_MSG)

    content = get_content(file_name=result.article.content_path)

    return get_translation(request=ContentTranslationRequest(content, result.language))

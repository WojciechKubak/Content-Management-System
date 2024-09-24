from translations.config.settings.messaging import TRANSLATED_ARTICLES_TOPIC
from translations.db.repositories import (
    language_repository,
    translation_repository,
    article_repository,
)
from translations.config.settings.storages import STORAGE_TYPE_STRATEGY
from translations.enums.enums import StorageType
from translations.integrations.aws.client import text_to_file_upload, file_get_content
from translations.common.services import (
    text_to_local_file_upload,
    file_get_local_content,
    file_name_generate,
)
from translations.config.settings.translations import TRANSLATION_TYPE_STRATEGY
from translations.enums.enums import TranslationType
from translations.common.services import content_get_local_translation
from translations.integrations.gpt.client import (
    BaseTranslationRequest,
    TitleTranslationRequest,
    ContentTranslationRequest,
    content_get_translation,
)
from translations.messaging.producers import TranslationResponse, message_produce
from translations.messaging.consumers import TranslationRequest
from translations.services.dtos import (
    TranslationDTO,
    ListTranslationDTO,
)
from translations.db.entities import Translation
from translations.core.exceptions import ValidationError


TRANSLATION_NOT_FOUND_ERROR_MSG: str = "Translation not found"
LANGUAGE_NOT_FOUND_ERROR_MSG: str = "Language not found"
TRANSLATION_NOT_PENDING_ERROR_MSG: str = "Translation is not pending"
TRANSLATION_ALREADY_EXISTS_ERROR_MSG: str = "Translation already exists"
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


def get_translation(*, request: BaseTranslationRequest) -> str:
    if TRANSLATION_TYPE_STRATEGY == TranslationType.LOCAL:
        return content_get_local_translation(request.content, request.language)
    else:
        return content_get_translation(request=request)


def translation_find_by_id(*, translation_id: int) -> TranslationDTO:
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


def translations_find_by_language(*, language_id: int) -> list[ListTranslationDTO]:
    if not language_repository.find_by_id(language_id):
        raise ValidationError(LANGUAGE_NOT_FOUND_ERROR_MSG)

    result = translation_repository.find_by_language(language_id)

    return [ListTranslationDTO.from_entity(translation) for translation in result]


def translations_get_all() -> list[ListTranslationDTO]:
    result = translation_repository.find_all()
    return [ListTranslationDTO.from_entity(translation) for translation in result]


def translation_content_change(
    *, translation_id: int, new_content: str
) -> TranslationDTO:
    result = translation_repository.find_by_id(translation_id)

    if not result:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    if result.status != Translation.StatusType.PENDING:
        raise ValidationError(TRANSLATION_NOT_PENDING_ERROR_MSG)

    if result.content_path:
        file_upload(file_name=result.content_path, content=new_content)
    else:
        file_name = file_name_generate()
        result.content_path = file_upload(file_name=file_name, content=new_content)
        translation_repository.save_or_update(result)

    content = get_content(file_name=result.article.content_path)

    return TranslationDTO.from_entity(result).with_contents(content, new_content)


def translation_title_change(*, translation_id: int, new_title: str) -> TranslationDTO:
    result = translation_repository.find_by_id(translation_id)

    if not result:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    if result.status != Translation.StatusType.PENDING:
        raise ValidationError(TRANSLATION_NOT_PENDING_ERROR_MSG)

    result.title = new_title
    translation_repository.save_or_update(result)

    original_content = get_content(file_name=result.article.content_path)
    translation_content = (
        get_content(file_name=result.content_path) if result.content_path else None
    )
    return TranslationDTO.from_entity(result).with_contents(
        original_content, translation_content
    )


def translation_status_change(
    *, translation_id: int, status: str, redactor_id: int
) -> ListTranslationDTO:
    result = translation_repository.find_by_id(translation_id)

    if not result:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    if result.status == Translation.StatusType.RELEASED:
        raise ValidationError(TRANSLATION_ALREADY_RELEASED_ERROR_MSG)

    match Translation.StatusType[status.upper()]:

        case Translation.StatusType.REQUESTED:
            result.translator_id = None
            result.status = Translation.StatusType.REQUESTED

        case Translation.StatusType.PENDING:
            result.translator_id = redactor_id
            result.status = Translation.StatusType.PENDING

        case Translation.StatusType.COMPLETED:
            result.status = Translation.StatusType.COMPLETED

        case Translation.StatusType.RELEASED:
            result.status = Translation.StatusType.RELEASED
            message_produce(
                TRANSLATED_ARTICLES_TOPIC,
                TranslationResponse.from_entity(result),
            )

        case Translation.StatusType.REJECTED:
            result.status = Translation.StatusType.REJECTED
            result.translator_id = None

    translation_repository.save_or_update(result)

    return ListTranslationDTO.from_entity(result)


def title_prepare_translation(*, translation_id: int) -> str:
    result = translation_repository.find_by_id(translation_id)

    if not result:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    if result.status != Translation.StatusType.PENDING:
        raise ValidationError(TRANSLATION_NOT_PENDING_ERROR_MSG)

    return get_translation(
        request=TitleTranslationRequest(result.title, result.language)
    )


def content_prepare_translation(*, translation_id: int) -> str:
    result = translation_repository.find_by_id(translation_id)

    if not result:
        raise ValidationError(TRANSLATION_NOT_FOUND_ERROR_MSG)

    if result.status != Translation.StatusType.PENDING:
        raise ValidationError(TRANSLATION_NOT_PENDING_ERROR_MSG)

    content = get_content(file_name=result.article.content_path)

    return get_translation(request=ContentTranslationRequest(content, result.language))


def handle_translation_request(
    *,
    translation_request: TranslationRequest,
) -> None:
    # todo: make this kwarg arguments only
    if not language_repository.find_by_id(translation_request.language_id):
        raise ValidationError(LANGUAGE_NOT_FOUND_ERROR_MSG)
    if translation_repository.find_by_language_and_article(
        translation_request.language_id,
        translation_request.id_,
    ):
        raise ValidationError(TRANSLATION_ALREADY_EXISTS_ERROR_MSG)

    article = article_repository.find_by_id(translation_request.id_)
    if not article:
        article = article_repository.save_or_update(
            translation_request.to_article_entity()
        )

    translation_repository.save_or_update(translation_request.to_translation_entity())

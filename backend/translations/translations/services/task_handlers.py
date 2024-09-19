from translations.integrations.kafka.consumer import TranslationRequest
from translations.persistance.repository import (
    language_repository,
    translation_repository,
    article_repository,
)
from translations.core.exceptions import ValidationError


LANGUAGE_NOT_FOUND_ERROR_MSG: str = "Language not found"
TRANSLATION_ALREADY_EXISTS_ERROR_MSG: str = "Translation already exists"


def handle_translation_request(
    translation_request: TranslationRequest,
) -> None:
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

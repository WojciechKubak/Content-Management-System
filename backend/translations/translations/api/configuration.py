from translations.env_config import (
    TRANSLATED_ARTICLES_TOPIC,
    TRANSLATIONS_SUBFOLDER_NAME,
)
from translations.persistance.repository import (
    language_repository,
    translation_repository,
)
from translations.broker.configuration import kafka_service
from translations.api.service import ApiService


api_service = ApiService(
    language_repository,
    translation_repository,
    kafka_service,
    TRANSLATED_ARTICLES_TOPIC,
    TRANSLATIONS_SUBFOLDER_NAME,
)

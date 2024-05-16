from translations.env_config import TRANSLATED_ARTICLES_TOPIC, TRANSLATIONS_SUBFOLDER_NAME
from translations.persistance.repository import language_repository, translation_repository
from translations.broker.configuration import kafka_service
from translations.storage.configuration import boto3_service
from translations.gpt.configuration import chat_gpt_service
from translations.api.service import ApiService


api_service = ApiService(
    language_repository, 
    translation_repository, 
    kafka_service, 
    boto3_service,
    chat_gpt_service,
    TRANSLATED_ARTICLES_TOPIC,
    TRANSLATIONS_SUBFOLDER_NAME
)

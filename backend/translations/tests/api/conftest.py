from translations.persistance.repository import TranslationRepository, LanguageRepository
from translations.api.service import ApiService
from translations.broker.kafka import KafkaService
from translations.storage.boto3 import Boto3Service
from translations.gpt.chat_gpt import ChatGPTService
from translations.api.service import ApiService
from unittest.mock import patch
from typing import Generator
import pytest


@pytest.fixture(scope='session')
def api_service(
    language_repository: LanguageRepository,
    translation_repository: TranslationRepository,
    kafka_service: KafkaService,
    boto3_service: Boto3Service,
    chat_gpt_service: ChatGPTService
) -> ApiService:
    return ApiService(
        language_repository, 
        translation_repository, 
        kafka_service,
        boto3_service, 
        chat_gpt_service,
        'test_translated_articles_topic', 
        'test_translations_subfolder'
    )


@pytest.fixture(scope='session', autouse=True)
def mock_api_service(api_service: ApiService) -> Generator[ApiService, None, None]:
    with patch('translations.api.routes.api_service', new=api_service):
        yield

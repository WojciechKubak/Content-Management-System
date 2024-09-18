from translations.env_config import BROKER_URI, GROUP_ID
from translations.broker.kafka import KafkaService
from translations.broker.consumer import EventConsumerService
from translations.persistance.repository import (
    language_repository,
    translation_repository,
    article_repository,
)

kafka_service = KafkaService(BROKER_URI, GROUP_ID)
consumer_handler_service = EventConsumerService(
    language_repository, translation_repository, article_repository
)

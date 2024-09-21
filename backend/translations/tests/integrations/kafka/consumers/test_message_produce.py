from translations.integrations.kafka.producers import (
    TranslationResponse,
    kafka_get_producer,
)
from unittest.mock import patch, MagicMock
from typing import Generator
import pytest
import json


def message_produce(topic_name: str, translation_response: TranslationResponse) -> None:
    producer = kafka_get_producer()
    producer.produce(
        topic_name, json.dumps(translation_response.to_dict()).encode("utf-8")
    )
    producer.flush()


@pytest.fixture
def mock_kafka_get_credentials() -> Generator:
    with patch(
        "translations.integrations.kafka.producers.kafka_get_credentials"
    ) as mock:
        yield mock


@pytest.fixture
def mock_producer() -> Generator:
    with patch("translations.integrations.kafka.producers.Producer") as mock:
        yield mock


def test_message_produce(mock_kafka_get_credentials, mock_producer) -> None:
    mock_kafka_get_credentials.return_value = MagicMock(boostrap_server="test_server")
    mock_producer_instance = MagicMock()
    mock_producer.return_value = mock_producer_instance

    translation_response = TranslationResponse(
        id_=1,
        title="test_title",
        content_path="test_path",
        language_id=1,
        translator_id=1,
    )

    message_produce("test_topic", translation_response)

    mock_producer_instance.produce.assert_called_once_with(
        "test_topic", json.dumps(translation_response.to_dict()).encode("utf-8")
    )
    mock_producer_instance.flush.assert_called_once()

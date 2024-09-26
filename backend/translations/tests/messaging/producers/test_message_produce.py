from translations.messaging.producers import (
    TranslationResponse,
    Producer,
    message_produce,
)
from unittest.mock import patch, MagicMock
import json


@patch("translations.messaging.producers.kafka_get_producer")
def test_message_produce_on_success_sends_serialized_response_to_broker(
    mock_kafka_get_producer,
) -> None:
    mock_producer = MagicMock(spec=Producer)
    mock_kafka_get_producer.return_value = mock_producer

    mock_translation_response = MagicMock(spec=TranslationResponse)
    mock_translation_response.to_dict.return_value = {}

    message_produce("topic", mock_translation_response)

    mock_kafka_get_producer.assert_called_once()
    mock_producer.produce.assert_called_once_with(
        "topic", json.dumps(mock_translation_response.to_dict()).encode("utf-8")
    )
    mock_producer.flush.assert_called_once()

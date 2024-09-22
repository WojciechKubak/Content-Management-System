from translations.messaging.producers import kafka_get_producer
from unittest.mock import patch


@patch("translations.messaging.producers.BROKER_URI", "test_broker_uri")
@patch("translations.messaging.producers.Producer")
def test_kafka_get_producer_on_success_uses_env__and_returns_producer_obj(
    mock_producer,
) -> None:
    kafka_get_producer()
    mock_producer.assert_called_once_with({"bootstrap.servers": "test_broker_uri"})

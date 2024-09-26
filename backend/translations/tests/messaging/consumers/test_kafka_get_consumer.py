from translations.messaging.consumers import kafka_get_consumer
from unittest.mock import patch


@patch("translations.messaging.consumers.BROKER_URI", "test_broker_uri")
@patch("translations.messaging.consumers.GROUP_ID", "test_group_id")
@patch("translations.messaging.consumers.Consumer")
def test_kafka_get_consumer_on_success_uses_env_and_returns_consumer_obj(
    mock_consumer,
) -> None:
    kafka_get_consumer()
    mock_consumer.assert_called_once_with(
        {
            "bootstrap.servers": "test_broker_uri",
            "group.id": "test_group_id",
            "auto.offset.reset": "earliest",
        }
    )

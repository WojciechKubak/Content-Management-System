from unittest.mock import patch, MagicMock
from translations.broker.kafka import KafkaService


@patch("translations.broker.kafka.Producer")
def test_produce_message(mock_producer_class):
    mock_producer_instance = mock_producer_class.return_value
    service = KafkaService(
        bootstrap_servers="test_bootstrap_server", group_id="test_group"
    )
    mock_dto_class = MagicMock()
    mock_dto_class.to_dict.return_value = {"key": "value"}

    service.produce_message("test_topic", mock_dto_class)

    mock_producer_instance.produce.assert_called_once_with(
        "test_topic", '{"key": "value"}'.encode("utf-8")
    )
    mock_producer_instance.flush.assert_called_once()

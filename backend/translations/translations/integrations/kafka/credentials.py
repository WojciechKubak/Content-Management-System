from translations.common.utils import assert_settings
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class KafkaConsumerCredentials:
    boostrap_server: str
    group_id: str


@lru_cache
def kafka_get_credentials() -> KafkaConsumerCredentials:
    settings = assert_settings(
        ["BROKER_URI", "GROUP_ID"],
        "Kafka credentials not found",
    )
    return KafkaConsumerCredentials(
        boostrap_server=settings["BROKER_URI"], group_id=settings["GROUP_ID"]
    )

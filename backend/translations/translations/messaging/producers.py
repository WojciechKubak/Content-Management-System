from translations.config.settings.messaging import BROKER_URI
from translations.db.entities import Translation
from confluent_kafka import Producer
from dataclasses import dataclass
from typing import Self, Any
import json


@dataclass
class TranslationResponse:
    id_: int
    title: str
    content_path: str
    language_id: int
    translator_id: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id_,
            "language_id": self.language_id,
            "title": self.title,
            "content_path": self.content_path,
            "translator_id": self.translator_id,
        }

    @classmethod
    def from_entity(cls, entity: Translation) -> Self:
        return cls(
            id_=entity.article_id,
            language_id=entity.language_id,
            title=entity.title,
            content_path=entity.content_path,
            translator_id=entity.translator_id,
        )


def kafka_get_producer() -> Producer:
    return Producer({"bootstrap.servers": BROKER_URI})


def message_produce(topic_name: str, translation_response: TranslationResponse) -> None:
    producer = kafka_get_producer()
    producer.produce(
        topic_name, json.dumps(translation_response.to_dict()).encode("utf-8")
    )
    producer.flush()

from translations.persistance.entity import Article, Translation
from translations.integrations.kafka.credentials import kafka_get_credentials
from confluent_kafka import Consumer
from typing import Callable, Type
from dataclasses import dataclass
from datetime import datetime
from typing import Self, Any
import logging
import json


@dataclass
class TranslationRequest:
    id_: int
    title: str
    content_path: str
    language_id: int
    date: datetime

    def to_article_entity(self) -> Article:
        return Article(id=self.id_, title=self.title, content_path=self.content_path)

    def to_translation_entity(self) -> Translation:
        return Translation(
            article_id=self.id_, requested_at=self.date, language_id=self.language_id
        )

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> Self:
        return cls(
            id_=data["id"],
            title=data["title"],
            content_path=data["content_path"],
            language_id=data["language_id"],
            date=data["date"],
        )


def kafka_get_consumer() -> Consumer:
    credentials = kafka_get_credentials()
    return Consumer(
        {
            "bootstrap.servers": credentials.boostrap_server,
            "group.id": credentials.group_id,
            "auto.offset.reset": "earliest",
        }
    )


def consume_messages(
    topic_name: str,
    handler: Callable[[Type], None],
    translation_request: TranslationRequest,
) -> None:
    consumer = kafka_get_consumer()
    consumer.subscribe([topic_name])

    logging.info(f"Consuming messages from topic: {topic_name}")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logging.info(f"Consumer error: {msg.error()}")
            continue

        data = json.loads(msg.value().decode("utf-8"))
        logging.info(f"Received message: {data}")

        try:
            handler(translation_request.from_dto(data))
            logging.info("Successfully handled")
        except Exception as e:
            logging.error(f"Error occured: {e}")
            continue

    consumer.close()

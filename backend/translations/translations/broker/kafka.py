from confluent_kafka import Producer, Consumer
from dataclasses import dataclass
from typing import Callable, Type
import logging
import json


@dataclass
class KafkaService:
    """
    A service class that handles producing and consuming messages with Kafka.

    Attributes:
        bootstrap_servers (str): The Kafka bootstrap servers.
        group_id (str): The consumer group id.
    """

    bootstrap_servers: str
    group_id: str

    def produce_message(self, topic_name: str, dto_class: Type) -> None:
        """
        Produces a message to a Kafka topic.

        This method creates a Kafka producer, produces a message to the specified topic, and then flushes the producer.

        Args:
            topic_name (str): The name of the Kafka topic.
            dto_class (Type): The DTO class to be serialized and sent as a message.
        """
        producer = Producer({"bootstrap.servers": self.bootstrap_servers})
        producer.produce(topic_name, json.dumps(dto_class.to_dict()).encode("utf-8"))
        producer.flush()

    def consume_messages(
        self, topic_name: str, handler: Callable[[Type], None], dto_class: Type
    ) -> None:
        """
        Consumes messages from a Kafka topic.

        This method creates a Kafka consumer, subscribes to the specified topic, and continuously polls for new messages.
        When a new message is received, it calls the provided handler function with the deserialized message.

        Args:
            topic_name (str): The name of the Kafka topic.
            handler (Callable[[Type], None]): The function to be called when a new message is received.
            dto_class (Type): The DTO class to be deserialized from received messages.

        Note:
            This method runs an infinite loop and should be run in a separate thread or process.
        """
        consumer = Consumer(
            {
                "bootstrap.servers": self.bootstrap_servers,
                "group.id": self.group_id,
                "auto.offset.reset": "earliest",
            }
        )
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
                handler(dto_class.from_dto(data))
                logging.info("Successfully handled")
            except Exception as e:
                logging.error(f"Error occured: {e}")
                continue

        consumer.close()

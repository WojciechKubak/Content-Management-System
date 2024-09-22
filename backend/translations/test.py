import json
from dataclasses import dataclass, asdict
from datetime import datetime
from confluent_kafka import Producer
import json
from dataclasses import dataclass
from datetime import datetime
from confluent_kafka import Consumer, KafkaException, KafkaError


@dataclass
class TranslationRequest:
    id: int
    title: str
    content_path: str
    language_id: int
    date: datetime


def delivery_report(err, msg):
    """Callback function called once for each message produced to indicate delivery result."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def produce_message():
    # Konfiguracja producenta Kafka
    conf = {"bootstrap.servers": "localhost:9091", "client.id": "group1"}

    producer = Producer(conf)

    # Tworzenie przykładowego obiektu TranslationRequest
    translation_request = TranslationRequest(
        id=1,
        title="Example Title",
        content_path="/path/to/content",
        language_id=2,
        date=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    )

    # Serializacja obiektu do formatu JSON
    message = json.dumps(asdict(translation_request))

    # Wysłanie wiadomości do Kafka
    topic = "translation_requests"
    producer.produce(topic, message, callback=delivery_report)

    # Czekanie na zakończenie wysyłania wiadomości
    producer.flush()


def consume_messages():
    # Konfiguracja konsumenta Kafka
    conf = {
        "bootstrap.servers": "localhost:9091",
        "group.id": "translation-consumer-group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(conf)

    # Subskrypcja do tematu
    topic = "translation_requests"
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached {msg.partition()}")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Deserializacja wiadomości z formatu JSON
                message = json.loads(msg.value().decode("utf-8"))
                translation_request = TranslationRequest(**message)
                print(f"Received message: {translation_request}")

    except KeyboardInterrupt:
        pass
    finally:
        # Zamknięcie konsumenta
        consumer.close()


if __name__ == "__main__":
    produce_message()
    # consume_messages()

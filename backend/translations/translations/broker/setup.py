from translations.env_config import TRANSLATION_REQUESTS_TOPIC, LANGUAGE_CHANGES_TOPIC
from translations.broker.configuration import kafka_service, consumer_handler_service
from translations.broker.dto import ArticleTranslationRequestDTO, LanguageEventDTO
from flask import Flask, Response, make_response
from flask_executor import Executor


def setup_start_pooling(app: Flask, executor: Executor) -> None:
    """Sets up a route in the Flask application to start consuming messages from Kafka topics."""

    @app.route("/start")
    def start_pooling() -> Response:
        """
        Starts consuming messages from Kafka topics.

        This function is the handler for the '/start' route. It starts two background tasks that consume messages
        from the 'TRANSACTION_REQUESTS_TOPIC' and 'LANGUAGE_CHANGES_TOPIC' Kafka topics. The messages are then
        handled by the 'handle_translation_request' and 'handle_language_event' methods of the
        'consumer_handler_service'.

        Returns:
            Response: A Flask Response object with a success message and a 200 status code.
        """
        executor.submit(
            kafka_service.consume_messages,
            TRANSLATION_REQUESTS_TOPIC,
            consumer_handler_service.handle_translation_request,
            ArticleTranslationRequestDTO,
        )
        executor.submit(
            kafka_service.consume_messages,
            LANGUAGE_CHANGES_TOPIC,
            consumer_handler_service.handle_language_event,
            LanguageEventDTO,
        )

        return make_response({"message": "Started"}, 200)

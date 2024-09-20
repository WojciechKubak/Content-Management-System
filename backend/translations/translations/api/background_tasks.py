from translations.config.config import TRANSLATION_REQUESTS_TOPIC
from translations.services.task_handlers import (
    handle_translation_request,
)
from translations.integrations.kafka.consumer import (
    TranslationRequest,
    consume_messages,
)
from flask import Flask, Response, make_response
from flask_executor import Executor


def register_background_tasks(app: Flask, executor: Executor) -> None:

    @app.route("/start")
    def start_pooling() -> Response:
        executor.submit(
            consume_messages,
            TRANSLATION_REQUESTS_TOPIC,
            handle_translation_request,
            TranslationRequest,
        )

        return make_response({"message": "Started"}, 200)

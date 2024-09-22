from translations.config.config import TRANSLATION_REQUESTS_TOPIC
from translations.services.handlers import handle_translation_request
from translations.integrations.kafka.consumers import (
    TranslationRequest,
    consumer_loop_start,
)
from flask import Flask, Response, make_response
from flask_executor import Executor


def background_tasks_register(app: Flask, executor: Executor) -> None:

    @app.route("/start")
    def start_pooling() -> Response:
        executor.submit(
            consumer_loop_start,
            TRANSLATION_REQUESTS_TOPIC,
            handle_translation_request,
            TranslationRequest,
        )

        return make_response({"message": "Started"}, 200)

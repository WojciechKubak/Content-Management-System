import os


BROKER_URI = os.getenv("BROKER_URI", "kafka1:9091")
GROUP_ID = os.getenv("GROUP_ID", "group1")
TRANSLATED_ARTICLES_TOPIC = os.getenv(
    "TRANSLATED_ARTICLES_TOPIC", "translated_articles"
)
TRANSLATION_REQUESTS_TOPIC = os.getenv(
    "TRANSLATION_REQUESTS_TOPIC", "translation_requests"
)

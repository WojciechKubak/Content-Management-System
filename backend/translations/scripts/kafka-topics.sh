#!/bin/bash

BROKER_URI=${BROKER_URI:-"kafka1:19091"}
TRANSLATED_ARTICLES_TOPIC=${TRANSLATED_ARTICLES_TOPIC:-"translated_articles"}
TRANSLATION_REQUESTS_TOPIC=${TRANSLATION_REQUESTS_TOPIC:-"translation_requests"}

echo "Topics before creation:"
kafka-topics --list --bootstrap-server $BROKER_URI

kafka-topics --create --topic $TRANSLATED_ARTICLES_TOPIC --bootstrap-server $BROKER_URI --partitions 1 --replication-factor 1
kafka-topics --create --topic $TRANSLATION_REQUESTS_TOPIC --bootstrap-server $BROKER_URI --partitions 1 --replication-factor 1

echo "Topics after creation:"
kafka-topics --list --bootstrap-server $BROKER_URI

echo "Topics created successfully."

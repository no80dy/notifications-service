#!/usr/bin/env bash

echo -e "Creating Kafka topics"
kafka-topics.sh --bootstrap-server kafka-0:9092 --create --if-not-exists --topic notification_events --replication-factor 3 --partitions 3
kafka-topics.sh --bootstrap-server kafka-0:9092 --create --if-not-exists --topic personal-film-selection --replication-factor 3 --partitions 3
kafka-topics.sh --bootstrap-server kafka-0:9092 --create --if-not-exists --topic new-films-release --replication-factor 3 --partitions 3
kafka-topics.sh --bootstrap-server kafka-0:9092 --create --if-not-exists --topic welcome-message --replication-factor 3 --partitions 3

#!/usr/bin/env bash

KAFKA_BROKERS=("kafka-0:9092" "kafka-1:9092" "kafka-2:9092")
RABBITMQ_BROKERS=("stats:5672" "queue-disc1:5672" "queue-ram1:5672")

MAX_ATTEMPTS=30

exponential_backoff() {
    local broker="$1"
    local attempt=0
    SLEEP_INTERVAL=1

    while [ $attempt -lt $MAX_ATTEMPTS ]; do
        nc -zv $broker 2>/dev/null

        if [ $? -eq 0 ]; then
            echo "Service $broker is ready!"
            return 0
        else
            echo "Attempt $((attempt + 1)): Service $broker not yet reachable. Retrying in $SLEEP_INTERVAL seconds..."
            sleep $SLEEP_INTERVAL
            ((attempt++))
            SLEEP_INTERVAL=$((2**attempt))
        fi
    done

    echo "Maximum attempts reached for service $broker. Service is still not fully reachable. Exiting..."
    return 1
}

check_kafka_cluster() {
    echo "Waiting for Kafka cluster to be ready..."

    for broker in "${KAFKA_BROKERS[@]}"; do
        exponential_backoff $broker || return 1
    done

    echo "All Kafka brokers are ready!"
    return 0
}

check_rabbitmq_cluster() {
  echo "Waiting for RabbitMQ cluster to be ready..."

  for node in "${RABBITMQ_BROKERS[@]}"; do
    exponential_backoff $node || return 1
  done

  echo "All RabbitMQ are ready!"
  return 0
}

check_kafka_cluster
check_rabbitmq_cluster

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

#!/usr/bin/env bash

POSTGRESQL_HOST="postgresql:5432"

MAX_ATTEMPTS=30

exponential_backoff() {
    local service="$1"
    local attempt=0
    SLEEP_INTERVAL=1

    while [ $attempt -lt $MAX_ATTEMPTS ]; do
        nc -zv $service 2>/dev/null

        if [ $? -eq 0 ]; then
            echo "Service $service is ready!"
            return 0
        else
            echo "Attempt $((attempt + 1)): Service $service not yet reachable. Retrying in $SLEEP_INTERVAL seconds..."
            sleep $SLEEP_INTERVAL
            ((attempt++))
            SLEEP_INTERVAL=$((2**attempt))
        fi
    done

    echo "Maximum attempts reached for service $service. Service is still not fully reachable. Exiting..."
    return 1
}

check_postgresql_node() {
    echo "Waiting for PostgreSQL node to be ready..."

    exponential_backoff $POSTGRESQL_HOST || return 1

    echo "All PostgreSQL node is ready!"
    return 0
}

check_postgresql_node

alembic revision --autogenerate -m "Init database"
alembic upgrade head

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

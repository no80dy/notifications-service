import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "ugc"

    mongodb_url: str = "mongodb://mongos1:27017"
    mongodb_database_name: str = "notificationsDb"
    mongodb_notifications_collection_name: str = "notifications"

    kafka_brokers: str = "kafka-0:9092,kafka-1:9092,kafka-2:9092"
    default_topic: str = "film_events"

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_login: str
    rabbitmq_password: str

    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"

    auth_service_url: str = "http://auth:8000/auth/api/v1/users"

    sentry_dsn: str


settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

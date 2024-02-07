import uuid

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    clickhouse_host: str = "clickhouse"
    clickhouse_port: int = 9000
    clickhouse_user: str = "default"

    producer_id: uuid.UUID = "84ab4a10-b44b-481d-acf0-50ca4313058d"
    notification_service_url: str = "http://notifications:8000/notifications/api/v1"


settings = Settings()

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "notification_worker"

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_login: str
    rabbitmq_password: str

    sentry_dsn: str


settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

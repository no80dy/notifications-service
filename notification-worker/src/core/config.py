import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "notification_worker"

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_login: str
    rabbitmq_password: str

    mailhog_host: str
    mailhog_port: int

    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"

    auth_service_url: str

    sentry_dsn: str


settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

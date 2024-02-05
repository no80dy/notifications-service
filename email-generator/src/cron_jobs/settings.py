from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    clickhouse_host: str = 'clickhouse'
    # clickhouse_host: str = 'localhost'
    clickhouse_port: int = 9000
    clickhouse_user: str = 'default'

    notification_service_url: str = 'http://notifications:8000/notifications/api/v1'


settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    max_emails_batch_size: int = 50
    notification_service_url: str = (
        "http://notifications:8000/notifications/api/v1/manager-message"
    )
    auth_service_url: str = "http://auth:8000/auth/api/v1/users/"


settings = Settings()

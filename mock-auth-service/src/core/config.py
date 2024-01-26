import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = 'auth'

    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_db: str = 'users'
    postgres_user: str = 'postgres'
    postgres_scheme: str = 'postgresql+asyncpg'


settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

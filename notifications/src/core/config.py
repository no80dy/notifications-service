import os

from pydantic_settings import BaseSettings
from logging import config as logging_config

from .logger import LOGGING


class Settings(BaseSettings):
	project_name: str = 'ugc'

	mongodb_url: str = 'mongodb://mongos1:27017'
	database_name: str = 'films_ugc'
	collection_name: str = 'events_ugc'

	kafka_brokers: str = 'kafka-0:9092,kafka-1:9092,kafka-2:9092'
	default_topic: str = 'film_events'

	rabbitmq_host: str
	rabbitmq_port: int
	rabbitmq_login: str
	rabbitmq_password: str

	sentry_dsn: str

settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
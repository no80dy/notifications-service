import logging

import requests
from clickhouse_driver import Client
from models import Notification
from requests.exceptions import ConnectionError, ConnectTimeout
from settings import settings


class NotificationHandler:
    def __init__(self):
        pass

    @staticmethod
    def sent_notification(url: str, notification: Notification) -> str:
        """Отправляет сообщение в сервис нотификации."""
        try:
            response = requests.post(url, data=notification.model_dump_json())
            return response.json()
        except ConnectionError or ConnectTimeout as e:
            logging.error(e)

    @staticmethod
    def get_data_from_clickhouse(query: str):
        """Достает данные из кликхауза на основании запроса."""
        batch_settings = {"max_block_size": 100000}
        try:
            with Client(
                host=settings.clickhouse_host, port=settings.clickhouse_port
            ) as client:
                results = client.execute_iter(query, settings=batch_settings)
                yield results
            return client.execute(query)
        except Exception as e:
            logging.error(e)

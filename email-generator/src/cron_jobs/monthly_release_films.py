import logging

import uuid
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from clickhouse_driver import Client

from settings import settings
from queries import monthly_release_films_sql

print('email generator with cron is working...')
HOW_MONTH_AGO = 1


class OutputFilmReleaseMessage(BaseModel):
    """
       Данная модель предназначена для ежемесячного
       оповещения всех пользователей о новых фильмах в кинотеатре за последний месяц.
   """
    notification_id: UUID = Field(default_factory=uuid.uuid4)
    event_name: str = 'films_release'
    film_ids: list[UUID]
    month_release: int = Field(ge=1, le=12)


def sent_notification(notification: OutputFilmReleaseMessage):
    """Отправляет сообщение в сервис нотификации."""
    try:
        response = requests.post(settings.notification_service_url, json=notification.model_dump_json())
        return response.text
    except ConnectionError or ConnectTimeout as e:
        logging.error(e)


def get_data_from_clickhouse(query: str):
    """Достает данные из кликхауза на основании запроса."""
    with Client(host=settings.clickhouse_host, port=settings.clickhouse_port) as client:
        try:
            return client.execute(query)
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    # Залезть в кликхаус и получить новые фильмы за предыдущий месяц
    month_ago = datetime.utcnow().month - HOW_MONTH_AGO
    query = monthly_release_films_sql.format(datetime.utcnow().replace(month=month_ago).strftime("%Y-%m-%d %H:%M:%S"))
    release_film_ids = [v[0] for v in get_data_from_clickhouse(query)]

    # Сформировать нотификацию
    if release_film_ids:
        message = OutputFilmReleaseMessage(
            film_ids=release_film_ids,
            month_release=datetime.utcnow().month
        )

        # Отправить в сервис нотификации
        print(sent_notification(message))

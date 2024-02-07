from datetime import datetime, timedelta

from handler import NotificationHandler
from models import OutputFilmSelectionMessage
from queries import weekly_favorite_films_users
from settings import settings

HOW_MANY_DAYS_AGO = 7
NOTIFICATION_URL = settings.notification_service_url + "/personal-film-selection"

if __name__ == "__main__":
    days_ago = datetime.utcnow() - timedelta(days=HOW_MANY_DAYS_AGO)
    query = weekly_favorite_films_users.format(days_ago.strftime("%Y-%m-%d %H:%M:%S"))
    results = NotificationHandler.get_data_from_clickhouse(query)
    if results:
        for batch in results:
            for data in batch:
                selection_user_id = data[0]
                selection_films_ids = [v for v in data[1]]

            # Сформировать нотификацию
            message = OutputFilmSelectionMessage(
                user_id=selection_user_id,
                producer_id=settings.producer_id,
                films_ids=selection_films_ids,
            )
            print(message.model_dump_json())
            # Отправить в сервис нотификации
            print(NotificationHandler.sent_notification(NOTIFICATION_URL, message))

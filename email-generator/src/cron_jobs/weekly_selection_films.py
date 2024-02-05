from datetime import datetime, timedelta

from handler import NotificationHandler
from queries import weekly_favorite_films_users, weekly_favorite_films_users2
from models import OutputFilmSelectionMessage

print('email generator with cron is working...')
HOW_MANY_DAYS_AGO = 7


if __name__ == '__main__':
    days_ago = datetime.utcnow() - timedelta(days=HOW_MANY_DAYS_AGO)
    query = weekly_favorite_films_users.format(days_ago.strftime("%Y-%m-%d %H:%M:%S"))
    results = NotificationHandler.get_data_from_clickhouse(query)
    if results:
        for result in results:
            selection_user_id = result[0]
            selection_films_ids = [v for v in result[1]]

            # Сформировать нотификацию
            message = OutputFilmSelectionMessage(
                user_id=selection_user_id,
                film_ids=selection_films_ids,
            )

            # Отправить в сервис нотификации
            print(NotificationHandler.sent_notification(message))

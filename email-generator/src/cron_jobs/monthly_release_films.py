from datetime import datetime

from handler import NotificationHandler
from models import OutputFilmReleaseMessage
from queries import monthly_release_films_sql, users_history
from settings import settings

HOW_MANY_MONTH_AGO = 1
NOTIFICATION_URL = settings.notification_service_url + "/new-films-release"


if __name__ == "__main__":
    # Залезть в кликхаус и получить новые фильмы за предыдущий месяц
    month_ago = datetime.utcnow().month - HOW_MANY_MONTH_AGO
    release_films_query = monthly_release_films_sql.format(
        datetime.utcnow().replace(month=month_ago).strftime("%Y-%m-%d %H:%M:%S")
    )
    results_release_films_query = NotificationHandler.get_data_from_clickhouse(
        release_films_query
    )
    for result in results_release_films_query:
        release_film_ids = [v[0] for v in result]

    users_history_query = users_history.format(
        datetime.utcnow().replace(month=month_ago).strftime("%Y-%m-%d %H:%M:%S")
    )
    results_users_history_query = NotificationHandler.get_data_from_clickhouse(
        users_history_query
    )
    for batch in results_users_history_query:
        for data in batch:
            user_id = data[0]
            watched_count = data[1]

            # Сформировать нотификацию
            message = OutputFilmReleaseMessage(
                user_id=user_id,
                films_ids=release_film_ids,
                producer_id=settings.producer_id,
                month_release=datetime.utcnow().month,
                watched_count=watched_count,
            )

            # Отправить в сервис нотификации
            print(NotificationHandler.sent_notification(NOTIFICATION_URL, message))

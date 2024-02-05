from datetime import datetime

from handler import NotificationHandler
from queries import monthly_release_films_sql
from models import OutputFilmReleaseMessage

print('email generator with cron is working...')
HOW_MANY_MONTH_AGO = 1


if __name__ == '__main__':
    # Залезть в кликхаус и получить новые фильмы за предыдущий месяц
    month_ago = datetime.utcnow().month - HOW_MANY_MONTH_AGO
    query = monthly_release_films_sql.format(datetime.utcnow().replace(month=month_ago).strftime("%Y-%m-%d %H:%M:%S"))
    results = NotificationHandler.get_data_from_clickhouse(query)
    for result in results:
        release_film_ids = [v[0] for v in result]

    # Сформировать нотификацию
    if release_film_ids:
        message = OutputFilmReleaseMessage(
            film_ids=release_film_ids,
            month_release=datetime.utcnow().month
        )

        # Отправить в сервис нотификации
        print(NotificationHandler.sent_notification(message))

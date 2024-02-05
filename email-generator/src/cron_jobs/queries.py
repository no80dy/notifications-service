users_history = """
    SELECT DISTINCT user_id, count(distinct film_id) AS watched_count
    FROM events.ugc_events
    WHERE event_name == 'film_history' AND created_at > '{}'
    GROUP BY user_id;
"""

monthly_release_films_sql = """
    SELECT film_id FROM events.ugc_events
    WHERE event_name == 'film_release' AND created_at > '{}'
    LIMIT 20;
"""

weekly_favorite_films_users = """
SELECT user_id, groupArray(film_id) AS film_ids
FROM events.ugc_events
WHERE event_name = 'film_favorites' AND created_at > '{}'
GROUP BY user_id;
"""

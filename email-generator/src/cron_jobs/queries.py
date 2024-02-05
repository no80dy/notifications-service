monthly_release_films_sql = """
    SELECT film_id FROM events.ugc_events
    WHERE event_name == 'film_release' AND created_at > '{}'
    LIMIT 20;
"""

weekly_favorite_films_users3 = """
    SELECT user_id, ARRAY_AGG(DISTINCT film_id) AS film_ids 
    FROM events.ugc_events
    WHERE event_name == 'film_favorites' AND created_at > '{}';
"""

weekly_favorite_films_users4 = """
SELECT user_id, arrayFilter(groupArrayArray((SELECT film_id FROM events.ugc_events WHERE event_name = ‘film_favorites’)), e -> notExists((SELECT film_id FROM events.ugc_events WHERE event_name = ‘film_history’), e)) AS film_ids FROM events.ugc_events GROUP BY user_id;"""

weekly_favorite_films_users7 = """
    SELECT t1.user_id, t1.film_id FROM events.ugc_events AS t1
    WHERE t1.event_name = 'film_favorites'
    AND t1.film_id NOT IN (SELECT t2.film_id FROM events.ugc_events AS t2 WHERE t2.event_name = 'film_history')
    GROUP BY t1.user_id, t1.film_id;
"""


weekly_favorite_films_users5 = """
SELECT user_id, groupArray(film_id -> notExists(_, 'film_history', film_id))
FROM events.ugc_events
WHERE event_name = 'film_favorites' AND created_at > '{}'
GROUP BY user_id;
"""

weekly_favorite_films_users = """
    SELECT user_id, groupArray(film_id) AS film_ids
    FROM events.ugc_events
    WHERE event_name = 'film_favorites' AND created_at > '{}' AND event_name == 'film_history'
    
    GROUP BY user_id;
"""

weekly_favorite_films_users2 = """
    SELECT * 
    FROM events.ugc_events AS t1 JOIN events.ugc_events AS t2
    ON t1.event_name = t2.event_name;
"""
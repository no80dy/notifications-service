monthly_release_films_sql = """
    SELECT film_id FROM events.ugc_events
    WHERE event_name == 'film_release' AND created_at > '{}'
    LIMIT 20;
"""

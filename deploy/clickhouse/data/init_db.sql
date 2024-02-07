CREATE DATABASE IF NOT EXISTS events;

CREATE TABLE IF NOT EXISTS events.ugc_events (
    id UUID,
    user_id UUID,
    film_id UUID,
    event_name String,
    comment Nullable(String),
    film_sec Nullable(Int64),
    score Nullable(Int64),
    created_at DateTime
) ENGINE = MergeTree()
ORDER BY id;

-- По нормальному пачкой почему-то не вставляет. Какой-то баг
-- event_name = 'film_release'
INSERT INTO events.ugc_events (event_name, film_id, created_at)
VALUES
('film_release', '1530ac24-8123-4db8-85ef-ccce5a3a37f1', '2024-01-10 00:00:00');
INSERT INTO events.ugc_events (event_name, film_id, created_at)
VALUES
('film_release', 'bb0be635-cafc-4102-bc00-531814aad57b', '2024-01-10 00:00:00');
INSERT INTO events.ugc_events (event_name, film_id, created_at)
VALUES
('film_release', '1c0dfb1c-f070-408b-b288-114e2d609a15', '2024-01-01 00:00:00');
INSERT INTO events.ugc_events (event_name, film_id, created_at)
VALUES
('film_release', 'cf84fb8d-d25a-41a3-987b-4d29861a00df', '2024-01-10 00:00:00');
INSERT INTO events.ugc_events (event_name, film_id, created_at)
VALUES
('film_release', '48fb7755-29c6-4b6d-9793-e5bdf7e18c1e', '2024-01-10 00:00:00');
INSERT INTO events.ugc_events (event_name, film_id, created_at)
VALUES
('film_release', 'c402b92d-1441-4c56-be4d-13d912141876', '2024-01-10 00:00:00');
INSERT INTO events.ugc_events (event_name, film_id, created_at)
VALUES
('film_release', '6cf128f0-e51c-433a-9656-897658aee0f9', '2024-01-10 00:00:00');
INSERT INTO events.ugc_events (event_name, film_id, created_at)
VALUES
('film_release', 'e47d3ebd-6827-4801-84cb-46afb73d86a7', '2024-01-10 00:00:00');
INSERT INTO events.ugc_events (event_name, film_id, created_at)
VALUES
('film_release', 'd847b846-f429-4f8e-a333-1558e5a91771', '2024-01-10 00:00:00');
INSERT INTO events.ugc_events (event_name, film_id, created_at)
VALUES
('film_release', '1111b483-63c4-4700-bf1a-c1ce51f40bf4', '2024-01-10 00:00:00');

-- event_name = 'film_history'
INSERT INTO events.ugc_events (event_name, user_id, film_id, film_sec, created_at)
VALUES
('film_history', '3fa85f64-5717-4562-b3fc-2c963f66afa6', '1530ac24-8123-4db8-85ef-ccce5a3a37f1', 1, '2024-02-05 00:00:00');

-- event_name = 'film_favorites'
INSERT INTO events.ugc_events (event_name, user_id, film_id, created_at)
VALUES
('film_favorites', '3fa85f64-5717-4562-b3fc-2c963f66afa6', '1530ac24-8123-4db8-85ef-ccce5a3a37f1', '2024-02-05 00:00:00');
INSERT INTO events.ugc_events (event_name, user_id, film_id, created_at)
VALUES
('film_favorites', '3fa85f64-5717-4562-b3fc-2c963f66afa6', 'bb0be635-cafc-4102-bc00-531814aad57b', '2024-02-05 00:00:00');
INSERT INTO events.ugc_events (event_name, user_id, film_id, created_at)
VALUES
('film_favorites', '3fa85f64-5717-4562-b3fc-2c963f66afa6', '1c0dfb1c-f070-408b-b288-114e2d609a15', '2024-02-05 00:00:00');

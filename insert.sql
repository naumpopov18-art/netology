INSERT INTO executors (name) VALUES 
('Исполнитель 1'),
('Исполнитель 2'),
('Исполнитель 3'),
('Исполнитель 4');

INSERT INTO genres (name) VALUES
('Жанр 1'),
('Жанр 2'),
('Жанр 3');

INSERT INTO albums (name, date) VALUES
('Альбом 1', '2020-10-10'),
('Альбом 2', '2021-10-10'),
('Альбом 3', '2022-10-10');

INSERT INTO tracks (name, duration, albumid) VALUES
('Трек 1', '100','1'),
('Трек 2', '112','2'),
('Трек 3', '543','3'),
('Трек 4', '543','1'),
('Трек 5', '254','2'),
('Трек 6', '126','3');

INSERT INTO collections (name, date) VALUES 
('Сборник 1', '2023-10-10'),
('Сборник 2', '2024-10-10'),
('Сборник 3', '2019-10-10'),
('Сборник 4', '2018-10-10');

INSERT INTO executorsgenre (genre_id, executor_id) VALUES
(1, 1),
(2, 1),
(2, 2),
(3, 3),
(1, 4);

INSERT INTO albumexecutor (album_id, executor_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(1, 4);

INSERT INTO collectiontrack (collection_id, track_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);
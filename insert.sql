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
('Альбом 1', '10/10/2020'),
('Альбом 2', '10/10/2021'),
('Альбом 3', '10/10/2022');

INSERT INTO tracks (name, duration, albumid) VALUES
('Трек 1', '100','1'),
('Трек 2', '112','2'),
('Трек 3', '543','3'),
('Трек 4', '543','1'),
('Трек 5', '254','2'),
('Трек 6', '126','3');

INSERT INTO collections (name, date) VALUES 
('Сборник 1', '10/10/2023'),
('Сборник 2', '10/10/2024'),
('Сборник 3', '10/10/2019'),
('Сборник 4', '10/10/2018');

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

INSERT INTO collectiontrack (collections_id, track_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);


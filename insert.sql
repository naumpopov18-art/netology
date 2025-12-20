INSERT INTO users (username) VALUES ('test_user');

INSERT INTO words (english_word, russian_word) VALUES 
('apple', 'яблоко'),
('cherry', 'вишня'),
('orange', 'апельсин'),
('juice', 'сок'),
('table', 'стол'),
('mouse', 'мышь'),
('listen', 'слушать'),
('talk', 'говорить'),
('run', 'бежать'),
('work', 'работать');


INSERT INTO "userWords" (user_id, word_id) VALUES 
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10);
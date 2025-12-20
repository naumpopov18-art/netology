CREATE TABLE IF NOT EXISTS users (
	userId SERIAL PRIMARY KEY,
	username VARCHAR
);

CREATE TABLE IF NOT EXISTS words (
	wordId SERIAL PRIMARY KEY,
	english_word VARCHAR,
	russian_word VARCHAR
);

CREATE TABLE IF NOT EXISTS userWords (
	userWordId SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users(userId),
	word_id INTEGER REFERENCES words(wordId),
	added_at DATE
)
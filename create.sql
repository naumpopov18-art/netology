create table if not exists genres(
	genreId SERIAL primary key,
	name VARCHAR(100)
);

create table if not exists albums(
	albumId SERIAL primary key,
	name VARCHAR(50),
	date DATE
);

create table if not exists tracks(
	trackId SERIAL primary key,
	name VARCHAR(100),
	duration INTEGER,
	albumId INTEGER references albums (albumId)
);

create table if not exists collections(
	collectionId SERIAL primary key,
	name VARCHAR(100),
	date DATE
);

create table if not exists executors(
	executorId SERIAL primary key,
	name VARCHAR(50)
);

create table if not exists albumExecutor(
	id SERIAL primary key,
	album_id INTEGER references albums (albumId),
	executor_id INTEGER references executors (executorId)
);

create table if not exists executorGenre(
	id SERIAL primary key,
	genre_id INTEGER references genres (genreId),
	executor_id INTEGER references executors (executorId)

);

create table if not exists collectionTrack(
	id SERIAL primary key,
	track_id INTEGER references tracks (trackId),
	collection_id INTEGER references collections (collectionId)
);

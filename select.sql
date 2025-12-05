SELECT name, duration
FROM tracks
ORDER BY duration DESC LIMIT 1

SELECT name, duration
FROM tracks
WHERE duration >= 210

SELECT name, date
FROM collections
WHERE EXTRACT(YEAR FROM TO_DATE(date, 'DD/MM/YYYY')) BETWEEN 2018 AND 2020;

SELECT name 
FROM executors 
WHERE name NOT LIKE '% %';

SELECT name 
FROM tracks 
WHERE name ILIKE '%мой%' OR name ILIKE '%my%';

SELECT genres.name, COUNT(executorGenre.executor_id)
FROM genres, executorGenre
WHERE genres.genreId = executorGenre.genre_id
GROUP BY genres.name;

SELECT COUNT(*)
FROM tracks, albums
WHERE tracks.albumId = albums.albumId
AND albums.date >= '2019-01-01' AND albums.date <= '2020-12-31';

SELECT albums.name, AVG(tracks.duration)
FROM albums, tracks
WHERE albums.albumId = tracks.albumId
GROUP BY albums.name;   

SELECT executors.name
FROM executors
WHERE executors.executorId NOT IN (
    SELECT albumExecutor.executor_id
    FROM albumExecutor, albums
    WHERE albumExecutor.album_id = albums.albumId
    AND EXTRACT(YEAR FROM albums.date) = 2020
);

SELECT collections.name
FROM collections, collectionTrack, tracks, albums, albumExecutor, executors
WHERE collections.collectionId = collectionTrack.collection_id
AND collectionTrack.track_id = tracks.trackId
AND tracks.albumId = albums.albumId
AND albums.albumId = albumExecutor.album_id
AND albumExecutor.executor_id = executors.executorId
AND executors.name = 'Worship';

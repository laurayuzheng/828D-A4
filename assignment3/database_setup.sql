CREATE USER cmsc828d;
CREATE DATABASE a3database;
\c a3database
ALTER USER cmsc828d WITH SUPERUSER;
SET ROLE cmsc828d;

CREATE TABLE anime(
	title text,
	type text,
	episodes integer,
	status text,
	start_airing date,
	end_airing date,
	starting_season text,
	broadcast_time integer,
	producers text[],
	licensors text[],
	studios text,
	sources text,
	genres text[],
	duration integer,
	rating text,
	score numeric,
	scored_by integer,
	members integer,
	num_favorites integer
);

COPY anime(title, type, episodes, status, start_airing,
	end_airing, starting_season, broadcast_time, producers,
	licensors, studios, sources, genres, duration,
	rating,
	score,
	scored_by,
	members,
	num_favorites)
FROM 'C:\Users\lyzheng\Desktop\spring2021\cmsc828d\assignment4\assignment3\anime_augmented.csv' 
DELIMITER ','
NULL AS 'null'
ENCODING 'UTF8'
CSV HEADER;

CREATE MATERIALIZED VIEW matview AS SELECT * FROM anime;

CREATE INDEX idx_start_airing ON matview(start_airing);

CREATE MATERIALIZED VIEW matviewsample AS SELECT d.*  
FROM (SELECT d.*,
			row_number() OVER (order by rating) AS seqnum,
			COUNT(*) OVER () AS cnt
		FROM anime d
	) d
WHERE seqnum % (cnt / 1000) = 1;

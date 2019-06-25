import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE "staging_events" (
    "artist" CHARACTER VARYING(200),
    "auth" CHARACTER VARYING(100),
    "firstName" CHARACTER VARYING(100),
    "gender" character,
    "iteminSession" INT,
    "lastName" CHARACTER VARYING(100),
    "length" decimal(10,5),
    "level" CHARACTER VARYING(25),
    "location" CHARACTER VARYING(200),
    "method" CHARACTER VARYING(25),
    "page" CHARACTER VARYING(25),
    "registration" DOUBLE PRECISION,
    "sessionId" INT,
    "song" CHARACTER VARYING(200),
    "status" INT,
    "ts" BIGINT,
    "userAgent" CHARACTER VARYING(200),
    "userId" INT
)
""")

staging_songs_table_create = ("""
CREATE TABLE "staging_songs" (
    "num_songs" INT,
    "artist_id" CHARACTER VARYING(100),
    "artist_latitude" decimal(10,5),
    "artist_longitude" decimal(10,5),
    "artist_location" CHARACTER VARYING(200),
    "artist_name" CHARACTER VARYING(200),
    "song_id" CHARACTER VARYING(100), 
    "title"CHARACTER VARYING(200), 
    "duration" decimal(10,5),
    "year" INT
)
""")

songplay_table_create = ("""
CREATE TABLE "songplays" (
	"songplay_id"	BIGINT IDENTITY(0,1) PRIMARY KEY,
	"start_time"	TIMESTAMP NOT NULL,
	"user_id"		INT NOT NULL REFERENCES users(user_id),
	"level"			CHARACTER VARYING(25),
	"song_id"		CHARACTER VARYING(100) REFERENCES songs(song_id),
	"artist_id"		CHARACTER VARYING(100) REFERENCES artists(artist_id),
	"session_id"	INT,
	"location"		CHARACTER VARYING(200),
	"user_agent"	CHARACTER VARYING(200))
""")

user_table_create = ("""
CREATE Table "users" (
	"user_id"		INT PRIMARY KEY,
	"first_name"	CHARACTER VARYING(100),
	"last_name"		CHARACTER VARYING(100),
	"gender"		character,
	"level"			CHARACTER VARYING(25)
) DISTSTYLE ALL;
""")

song_table_create = ("""
CREATE TABLE "songs" (
	"song_id"		CHARACTER VARYING(100) NOT NULL PRIMARY KEY,
	"title"			CHARACTER VARYING(200),
	"artist_id"		CHARACTER VARYING(100),
	"year"			INT,
	"duration"		DECIMAL(10,5)
) DISTSTYLE ALL;
""")

artist_table_create = ("""
CREATE TABLE "artists" (
	"artist_id"		CHARACTER VARYING(100) NOT NULL PRIMARY KEY,
	"name"			CHARACTER VARYING(200),
	"location"		CHARACTER VARYING(200),
	"latitude"		DECIMAL(10,5),
	"longitude"		DECIMAL(10,5)
) DISTSTYLE ALL;
""")


time_table_create = ("""
CREATE TABLE "time" (
	"start_time"	TIMESTAMP NOT NULL PRIMARY KEY,
	"hour"			INT,
	"day"			INT,
	"week"			INT,
	"month"			INT,
	"year"			INT,
	"weekday"		CHARACTER VARYING(10)
) DISTSTYLE ALL;
""")

# STAGING TABLES

staging_events_copy = ("""

copy staging_events from 's3://udacity-dend/log_data/' 
iam_role 'arn:aws:iam::493218832866:role/dwhRole'
region 'us-west-2' FORMAT AS JSON 's3://udacity-dend/log_json_path.json'

""").format()

staging_songs_copy = ("""

copy staging_songs from 's3://udacity-dend/song_data/'
iam_role 'arn:aws:iam::493218832866:role/dwhRole'
FORMAT AS JSON 'auto';

""").format()


# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays(start_time,user_id,level,song_id,artist_id,session_id,location,user_agent)
SELECT DISTINCT
TIMESTAMP 'epoch' + a1.ts/1000 *INTERVAL '1 second',
a1.userid,
a1.level,
a2.song_id,
a2.artist_id,
a1.sessionId,
a1.location,
a1.userAgent
FROM
staging_events a1
JOIN staging_songs a2 
on 	a1.song = a2.title and 
	a1.artist = a2.artist_name
WHERE a1.page = 'NextSong'
""")

user_table_insert = ("""
INSERT INTO users(user_id,first_name,last_name,gender,level)
SELECT DISTINCT
userid,
firstName,
lastName,
gender,
level
FROM staging_events
WHERE userid IS NOT NULL
""")

song_table_insert = ("""
INSERT INTO songs(song_id,title,artist_id,year,duration)
SELECT DISTINCT 
song_id,
title,
artist_id,
year,
duration
from staging_songs
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id,name,location,latitude,longitude)
SELECT DISTINCT
artist_id, 
artist_name,
artist_location,
artist_latitude, 
artist_longitude
FROM staging_songs
""")

time_table_insert = ("""
INSERT INTO time(start_time,hour,day,week,month,year,weekday)
SELECT DISTINCT
TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' AS START_TIME,
EXTRACT(HRS FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') AS HOUR,
EXTRACT(D FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') AS DAY,
EXTRACT(W FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') AS WEEK,
EXTRACT(MON FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') AS MONTH,
EXTRACT(Y FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') AS YEAR,
CASE 	WHEN EXTRACT(DOW FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')=0 THEN 'SUN' 
		WHEN EXTRACT(DOW FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')=1 THEN 'MON' 
		WHEN EXTRACT(DOW FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')=2 THEN 'TUES' 
		WHEN EXTRACT(DOW FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')=3 THEN 'WED' 
		WHEN EXTRACT(DOW FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')=4 THEN 'THUR' 
		WHEN EXTRACT(DOW FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')=5 THEN 'FRI' 
		WHEN EXTRACT(DOW FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')=6 THEN 'SAT' 
END AS WEEKDAY
FROM staging_events
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert,songplay_table_insert]

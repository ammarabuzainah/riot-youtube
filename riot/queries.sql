--first stream

CREATE STREAM video_data_stream (
    channel_id STRING,
    video_id STRING,
    user_id STRING,
    title STRING,
    description STRING,
    live_status STRING,
    category_id INT,
    views INT,
    likes INT,
    n_comments INT,
    duration DOUBLE,
    published_at BIGINT,
    tags ARRAY<STRING,
    active_program ARRAY<STRING
) WITH (
    KAFKA_TOPIC='youtube',
    VALUE_FORMAT='AVRO'
);
--video level query

CREATE Table video_statistics WITH (KAFKA_TOPIC='video_data_statistics', VALUE_FORMAT='AVRO', VALUE_SCHEMA_ID = 38, KEY_FORMAT='KAFKA') AS
SELECT
    LATEST_BY_OFFSET(channel_id) AS `channelId`,
    LATEST_BY_OFFSET(user_id) AS `userId`,
    LATEST_BY_OFFSET(live_status) AS `liveStatus`,
    LATEST_BY_OFFSET(category_id) AS `categoryId`,
    LATEST_BY_OFFSET(description) AS `description`,
    LATEST_BY_OFFSET(title) AS `title`,
    LATEST_BY_OFFSET(tags) AS `tags`,
    LATEST_BY_OFFSET(duration) AS `duration`,
    LATEST_BY_OFFSET(published_at) AS `publishedAt`,

    AVG(LIKES) AS `avgLikes`,
    AVG(views) AS `avgViews`,
    AVG(n_comments) AS `avgComments`,
    LATEST_BY_OFFSET(views) AS `latestViews`,
    LATEST_BY_OFFSET(n_comments) AS `latestComments`,
    LATEST_BY_OFFSET(likes) AS `latestLikes`,
    as_value (video_id) `videoId`, video_id as `vid`
FROM
    video_data_stream
GROUP BY
    video_id
EMIT CHANGES;


--user level
--first table

CREATE TABLE USER_STATISTICS WITH (KAFKA_TOPIC='row_user_data', VALUE_FORMAT='AVRO', VALUE_SCHEMA_ID = 72, KEY_FORMAT='KAFKA')
AS SELECT
    AVG(`latestLikes`) AS `avgLikes`,
    AVG(`latestViews`) AS `avgViews`,
    AVG(`latestComments`) AS `avgComments`,
    as_value (`userId`) `userId`, `userId` as `user`

FROM
    video_statistics
GROUP BY
    `userId`
EMIT CHANGES;

--second table:

CREATE TABLE USER_STATISTICS2 WITH (KAFKA_TOPIC='row_user_data2', VALUE_FORMAT='AVRO', VALUE_SCHEMA_ID = 94, KEY_FORMAT='KAFKA')
AS SELECT

SUM(DURATION) AS `totalDuration`,
COUNT_DISTINCT(VIDEO_ID) as `videoCount`,
as_value (user_id) `userId`, user_id as `user`
FROM VIDEO_DATA_STREAM

GROUP BY user_id
EMIT CHANGES;


--Join tables.. Didn't create a schema for this table

CREATE TABLE FULL_USER_STATISTICS
AS SELECT
    us.`userId` AS `userId`,
    us.`totalDuration`,
    us.`videoCount`,
    um.`avgLikes`,
    um.`avgViews`,
    um.`avgComments`
FROM USER_STATISTICS2 us
INNER JOIN USER_STATISTICS um ON us.`user` = um.`user`
EMIT CHANGES;

-------------------------------
--program level

#STEP ONE EXPLODE

create stream PROGRAM_LEVEL AS
select video_id, user_id, explode(active_program) as program_id,
duration, published_at, views,likes,n_comments,category_id from video_data_stream emit changes;

--STEP TWO CONCAT COLUMNS

CREATE STREAM PROGRAM_LEVEL_PART1 AS select *, CONCAT(user_id,'_', program_id)as user_program,
CONCAT(video_id,'_',program_id) as video_program from program_level;


--STEP THREE (A).. CREATE FINAL TABLE FOR USER_PROGRAM STATISTICS
CREATE TABLE USER_PROGRAM_STATISTICS AS
SELECT USER_PROGRAM,
LATEST_BY_OFFSET(VIEWS) AS latestViews,
LATEST_BY_OFFSET(LIKES) AS latestLikes,
LATEST_BY_OFFSET(N_COMMENTS) AS latestComments,
AVG(VIEWS) AS avgViews,
AVG(LIKES) AS avgLikes,
AVG(N_COMMENTS) AS avgComments,
COUNT_DISTINCT(VIDEO_ID) AS countVideos
FROM PROGRAM_LEVEL_PART1 GROUP BY(USER_PROGRAM) EMIT CHANGES;


--STEP THREE (B).. CREATE FINAL TABLE FOR VIDEO_PROGRAM
CREATE TABLE VIDEO_PROGRAM_STATISTICS AS
SELECT VIDEO_PROGRAM,
LATEST_BY_OFFSET(VIEWS) AS latestViews,
LATEST_BY_OFFSET(LIKES) AS latestLikes,
LATEST_BY_OFFSET(N_COMMENTS) AS latestComments,
AVG(VIEWS) AS avgViews,
AVG(LIKES) AS avgLikes,
AVG(N_COMMENTS) AS avgComments,
COUNT_DISTINCT(VIDEO_ID) AS countVideos

FROM PROGRAM_LEVEL_PART1 GROUP BY(VIDEO_PROGRAM) EMIT CHANGES;
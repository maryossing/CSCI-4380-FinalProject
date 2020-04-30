DROP SCHEMA IF EXISTS project CASCADE;
CREATE SCHEMA project;


DROP TABLE IF EXISTS Weather;
DROP TABLE IF EXISTS Standings;
DROP TABLE IF EXISTS Games;
CREATE TABLE Division(
    name VARCHAR(3)
);
CREATE TABLE Weather(
    gameid VARCHAR(123) PRIMARY KEY,
    temp INT,
    wind_chill INT,
    humidity INT,
    wind_speed INT,
    summary VARCHAR(511),
    date DATE

);
CREATE TABLE Games(
    gameid VARCHAR(123) PRIMARY KEY,
    home_team VARCHAR(255),
    home_id VARCHAR(3),
    home_score INT,
    away_team VARCHAR(255),
    away_id VARCHAR(3),
    away_score INT,
    date DATE

);
CREATE TABLE Standings(
	season INT,
	confrence VARCHAR(16),
	division VARCHAR(16),
	team VARCHAR(255),
	wins INT,
	losses INT,
	ties INT,
	winpct DECIMAL(6,5),
	div_rank INT,
	points_scored INT,
	points_allowed INT, 
	net_points INT,
	str_vict DECIMAL(6,5),
	str_sched DECIMAL(6,5),
	seed INT,
	playoff VARCHAR(255),
	PRIMARY KEY(season, team)
);

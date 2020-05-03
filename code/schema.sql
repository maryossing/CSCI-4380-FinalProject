DROP SCHEMA IF EXISTS project CASCADE;
CREATE SCHEMA project;

DROP TABLE IF EXISTS Conference CASCADE;
DROP TABLE IF EXISTS Team CASCADE;
DROP TABLE IF EXISTS Division CASCADE;
DROP TABLE IF EXISTS Game CASCADE;
DROP TABLE IF EXISTS Weather CASCADE;
DROP TABLE IF EXISTS Standings CASCADE;
DROP TABLE IF EXISTS Statistics;
DROP TABLE IF EXISTS Playoffs;
CREATE TABLE Conference
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(127) UNIQUE
);

CREATE TABLE Division
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(127) UNIQUE
);

CREATE TABLE Team
(
  id SERIAL PRIMARY KEY,
  initial VARCHAR(3) UNIQUE,
  name VARCHAR(127) UNIQUE,
  conference INTEGER REFERENCES Conference(id),
  division INTEGER REFERENCES Division(id)
);

CREATE TABLE Game
(
  id SERIAL PRIMARY KEY,
  home_team INTEGER REFERENCES Team(id),
  away_team INTEGER REFERENCES Team(id),
  home_score INTEGER,
  away_score INTEGER,
  game_date DATE
);

CREATE TABLE Weather
(
  game_id INTEGER REFERENCES Game(id),
  temp INTEGER,
  wind_chill INTEGER,
  humidity DECIMAL(5,2),
  wind_mph INTEGER,
  PRIMARY KEY (game_id)
);


CREATE TABLE Standings
(
  id SERIAL UNIQUE,
  season INTEGER,
  team_id INTEGER REFERENCES Team(id),
  wins INTEGER,
  losses INTEGER,
  ties INTEGER,
  pct DECIMAL(5,2),
  div_rank INTEGER,
  PRIMARY KEY (team_id, season)
);

CREATE TABLE Statistics
(
  standings_id INTEGER REFERENCES Standings(id),
  scored INTEGER,
  allowed INTEGER,
  net INTEGER,
  sov DECIMAL (7, 6), --Strength of Victory
  sos DECIMAL (7, 6), --Strength of Schedule
  PRIMARY KEY (standings_id)
);

--- This Table could still use some normalization can't think of a good way to do it rn
CREATE TABLE Playoffs
(
  standings_id INTEGER REFERENCES Standings(id),
  seed INTEGER,
  won_div BOOLEAN, -- Won Division
  won_conf BOOLEAN, -- Won Conference
  won_sb BOOLEAN, -- Won Superbowl
  PRIMARY KEY (standings_id)
);

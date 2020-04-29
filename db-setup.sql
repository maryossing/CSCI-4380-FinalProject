CREATE DATABASE dbms_final_project;
CREATE USER dbms_project_user WITH PASSWORD 'dbms_password';
GRANT ALL PRIVILEGES ON DATABASE dbms_final_project TO dbms_project_user;

\connect "dbname=dbms_final_project user=dbms_project_user password=dbms_password";

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
  name VARCHAR(255),
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
  won_wc BOOLEAN, -- Won Wildcard
  won_div BOOLEAN, -- Won Division
  won_conf BOOLEAN, -- Won Conference
  won_sb BOOLEAN, -- Won Superbowl
  PRIMARY KEY (standings_id)
);

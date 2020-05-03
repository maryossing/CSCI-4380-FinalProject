import psycopg2
import psycopg2.extras
connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
conn = psycopg2.connect(connection_string, cursor_factory=psycopg2.extras.DictCursor)
cursor = conn.cursor()



# creates queries to find a teams average points scored in windy games
def windy_queries(name):
	windy_away_points="SELECT sum(away_score),count(game_id) from game,team,weather where game.id=weather.game_id and wind_mph>=20 and away_team=team.id  and team.name=%s;"
	windy_away_wins="SELECT count(game_id) from game,team,weather where game.id=weather.game_id and wind_mph>=20 and away_team=team.id  and team.name=%s and home_score<away_score;"
	windy_home_points="SELECT sum(home_score),count(game_id) from game,team,weather where game.id=weather.game_id and wind_mph>=20 and home_team=team.id  and team.name=%s;"
	windy_home_wins="SELECT count(game_id) from game,team,weather where game.id=weather.game_id and wind_mph>=20 and home_team=team.id  and team.name=%s and home_score>away_score;"
	away_points="SELECT sum(away_score),count(game_id) from game,team,weather where game.id=weather.game_id and wind_mph<20 and away_team=team.id  and team.name=%s;"
	home_points="SELECT sum(home_score),count(game_id) from game,team,weather where game.id=weather.game_id and wind_mph<20 and home_team=team.id  and team.name=%s;"
	queries=[windy_away_points,windy_away_wins,windy_home_points,windy_home_wins,away_points,home_points]
	return weather_points(queries,name)

# creates queries to find a teams average points scored in cold games
def cold_queries(name):
	cold_away_points="SELECT sum(away_score),count(game_id) from game,team,weather where game.id=weather.game_id and (temp<32 or (wind_chill !=0 and wind_chill<32)) and away_team=team.id  and team.name=%s;"
	cold_away_wins="SELECT count(game_id) from game,team,weather where game.id=weather.game_id and (temp<32 or (wind_chill !=0 and wind_chill<32)) and away_team=team.id  and team.name=%s and home_score<away_score;"
	cold_home_points="SELECT sum(home_score),count(game_id) from game,team,weather where game.id=weather.game_id and (temp<32 or (wind_chill !=0 and wind_chill<32)) and home_team=team.id  and team.name=%s;"
	cold_home_wins="SELECT count(game_id) from game,team,weather where game.id=weather.game_id and (temp<32 or (wind_chill !=0 and wind_chill<32)) and home_team=team.id  and team.name=%s and home_score>away_score;"
	away_points="SELECT sum(away_score),count(game_id) from game,team,weather where game.id=weather.game_id and temp>32 and away_team=team.id  and team.name=%s;"
	home_points="SELECT sum(home_score),count(game_id) from game,team,weather where game.id=weather.game_id and temp>32 and home_team=team.id  and team.name=%s;"
	queries=[cold_away_points,cold_away_wins,cold_home_points,cold_home_wins,away_points,home_points]
	return weather_points(queries,name)

# creates queries to find a teams average points scored in warm games
def warm_queries(name):
	warm_away_points="SELECT sum(away_score),count(game_id) from game,team,weather where game.id=weather.game_id and temp>=80 and away_team=team.id  and team.name=%s;"
	warm_away_wins="SELECT count(game_id) from game,team,weather where game.id=weather.game_id and temp>=80 and away_team=team.id  and team.name=%s and home_score<away_score;"
	warm_home_points="SELECT sum(home_score),count(game_id) from game,team,weather where game.id=weather.game_id and temp>=80 and home_team=team.id  and team.name=%s;"
	warm_home_wins="SELECT count(game_id) from game,team,weather where game.id=weather.game_id and temp>=80 and home_team=team.id  and team.name=%s and home_score>away_score;"
	away_points="SELECT sum(away_score),count(game_id) from game,team,weather where game.id=weather.game_id and temp<80 and away_team=team.id  and team.name=%s;"
	home_points="SELECT sum(home_score),count(game_id) from game,team,weather where game.id=weather.game_id and temp<80 and home_team=team.id  and team.name=%s;"
	queries=[warm_away_points,warm_away_wins,warm_home_points,warm_home_wins,away_points,home_points]
	return weather_points(queries,name)

#processes sets of weather queries, calculating thedifference in average points scored and total games played in given extreme weather
def weather_points(queries,name):
	points=0
	games=0
	wins=0
	w_games=0
	w_points=0
	
	with conn.cursor() as cursor:
		cursor.execute(queries[0],(name,))
		ret=cursor.fetchall()
		if ret[0][1]!=0:
			w_points +=ret[0][0]
			w_games +=ret[0][1]

		cursor.execute(queries[1],(name,))
		ret=cursor.fetchall()
		wins+=ret[0][0]

		cursor.execute(queries[2],(name,))
		ret=cursor.fetchall()
		if ret[0][1]!=0:
			w_points+= ret[0][0]
			w_games +=ret[0][1]

		cursor.execute(queries[3],(name,))
		ret=cursor.fetchall()
		wins+=ret[0][0]

		cursor.execute(queries[4],(name,))
		ret=cursor.fetchall()
		if ret[0][1]!=0:
			points +=ret[0][0]
			games +=ret[0][1]

		cursor.execute(queries[5],(name,))
		ret=cursor.fetchall()
		if ret[0][1]!=0:
			points +=ret[0][0]
			games +=ret[0][1]

	
	avg_points=points/games
	avg_w_points=w_points/w_games
	#differece in average points
	diff=avg_points- avg_w_points
	return diff, w_games,wins	


#returns team name(s) that resemble the given name string
def find_team(name):
	name="%%"+name+"%%"
	query= "SELECT team.name FROM team WHERE team.name ILIKE %s;"
	with conn.cursor() as cursor:
		cursor.execute(query,(name,))
		return cursor.fetchall() 
#returns years a given team went to the playoffs
def playoffs_years(name):
	query ="SELECT season from standings, playoffs,team where team.name=%s and team.id=standings.team_id and standings.id=playoffs.standings_id and playoffs.seed is NOT NULL;"
	with conn.cursor() as cursor:
		cursor.execute(query,(name,))
		return cursor.fetchall()

#returns playoffs result for a given team in a given year
def playoffs_progress(name,year):
	#get result of divisional round
	query ="SELECT won_div from standings, playoffs,team where team.name=%s and team.id=standings.team_id and standings.id=playoffs.standings_id and season=%s ;"
	with conn.cursor() as cursor:
		cursor.execute(query,(name,year,))
		won= cursor.fetchall()[0][0]
	
		if won:
			#get result of confrence championship
			query ="SELECT won_conf from standings, playoffs,team where team.name=%s and team.id=standings.team_id and standings.id=playoffs.standings_id and season=%s ;"
			cursor.execute(query,(name,year,))
			won= cursor.fetchall()[0][0]
			if won:
				#get result of superbowl
				query ="SELECT won_sb from standings, playoffs,team where team.name=%s and team.id=standings.team_id and standings.id=playoffs.standings_id and season=%s ;"
				cursor.execute(query,(name,year,))
				won= cursor.fetchall()[0][0]
				if won:
					return "Won Super Bowl"
				else:
					return "Lost Super Bowl"
			else:
				return "Lost Conference Championships"
		else:
			return "Lost Divisional Championships"
#get season with highest strength of schedule for a given team
def get_hardest_season(name):
	query="SELECT season  from (select max(sos) as maxsos from standings, statistics,team where team.name=%s and team.id=standings.team_id \
	 and statistics.standings_id=standings.id) as seasons, standings,statistics,team where statistics.sos=maxsos and statistics.standings_id=standings.id \
	 and team.name=%s and team.id=standings.team_id;"
	with conn.cursor() as cursor:
		cursor.execute(query,(name,name,))
		
		return cursor.fetchall()[0][0]

#returns a given teams record in a given year
def get_record(team,year):
	query="SELECT wins, losses,ties FROM standings, team WHERE team.name=%s and season =%s and team.id=standings.team_id;"
	with conn.cursor() as cursor:
		cursor.execute(query,(team,year,))
		ret=cursor.fetchall()
		w=ret[0][0]
		l=ret[0][1]
		t=ret[0][2]
	return w,l,t
# returns a given teams rank in a given year
def get_rank(team,year):
	query="SELECT div_rank FROM standings, team WHERE team.name=%s and season =%s and team.id=standings.team_id;"
	with conn.cursor() as cursor:
		cursor.execute(query,(team,year,))
		return cursor.fetchall()[0][0]

#returns a given teams division
def get_division(team):
	query="SELECT division.name FROM  team,division WHERE team.name=%s and team.division=division.id;"
	with conn.cursor() as cursor:
		cursor.execute(query,(team,))
		ret=cursor.fetchall()
		return ret[0][0]

# returns list of (winner, loser, season) tuples for each super bowl a team participated in
def get_SuperBowls(team):
	query ="SELECT w.winner, l.loser,w.season from (SELECT team.name as winner,season from standings, playoffs,team where won_sb=TRUE \
	and team.id=standings.team_id and standings.id=playoffs.standings_id)as w,  (SELECT team.name as loser,season from \
	standings, playoffs,team where won_sb=FALSE and won_conf=TRUE and team.id=standings.team_id and standings.id=playoffs.standings_id)as l where w.season=l.season and (w.winner=%s or l.loser=%s) ;"
	with conn.cursor() as cursor:
		cursor.execute(query,(team,team,))
		print
		return cursor.fetchall()
		

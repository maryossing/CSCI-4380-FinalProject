from database import *

#print input options for a team
def print_menu(team):
	print("-"*50)
	print("What would you like to know about the {} from 2002-2013? ".format(team))
	print("  w - weather statistics")
	print("  p - playoff history")
	print("  d - most difficult season (according to strength of schedule)")
	print("  s - season statistics")
	print("  b - Super Bowls\n")
	print("  t - choose a different team")
	print("  q - quit application")

#prints a teams stats for a given season
def season_stats(team, year):

	w,l,t=get_record(team, year)
	rank=get_rank(team,year)
	if rank==1:
		rank=str(rank)+"st"
	elif rank==2:
		rank=str(rank)+"nd"
	elif rank==3:
		rank=str(rank)+"rd"
	else:
		rank=str(rank)+"th"
	div=get_division(team)
	print("The {} ended the {} regular season {}-{}-{}, {} in the {}".format(team, year, w,l,t,rank, div))

# prints a teams stats for games played in different weather extremes
def team_weather(team):
	points, games,wins=windy_queries(team)
	diff="fewer"
	if points<0:
		diff= "more"
	print("The {0} played {2} games with wind of at least 20mph winning {1} and scoring an average of {3:.2f} {4} points than non-windy games".format(team, wins,games, abs(points),diff))
	
	points, games,wins=cold_queries(team)
	diff="fewer"
	if points<0:
		diff= "more"
	print("The {0} played {2} games below freezing (with wind chill) winning {1} and scoring an average of {3:.2f} {4} points than in warmer games".format(team, wins,games, abs(points),diff))
	points, games,wins=warm_queries(team)
	diff="fewer"
	if points<0:
		diff= "more"
	print("The {0} played {2} games at 80+ degrees Fahrenheit winning {1} and scoring an average of {3:.2f} {4} points than in colder games".format(team, wins,games, abs(points),diff))

# prints Super Bowl teams and year that the given team participated in
def SuperBowl(team):
	games=get_SuperBowls(team)
	for game in games:
		print("At the end of the {2} season, the {0} beat the {1} in the Super Bowl".format(game[0], game[1], game[2]))
	if len(games)==0:
		print("The {} never went to the Super Bowl from 2002-2013".format(team))

# returns the full team name that resembles the input name
def check_name(input_name):
	teams=find_team(input_name)
	#if no team or more than one string resemble input name, return false
	if len(teams) ==0 or  len(teams)!=1:
		return False
	return teams[0][0]
# prints the years a team went to the playoffs and how far they made it
def playoffs_results(team):
	years=playoffs_years(team)
	if len(years)==0:
		print("The {} went to the playoffs {} times from 2002-2013".format(team,len(years)))
		return
	print("The {} went to the playoffs {} times from 2002-2013:".format(team,len(years)))

	#print each year and progress
	years=playoffs_years(team)
	for year in years:
		print("  ",year[0] ,"-", playoffs_progress(team,year[0]))

#prints the season where the team had the highest strength of schedule
def hardest_season(team):
	print("The {} had their most difficult season in {}".format(team,get_hardest_season(team)))

#asks user for a valid year from 2002-2013, returns year
def get_year():
	year=input("Enter a season (2002-2013) or type 'all' for all seaons => ")
	year=year.strip()
	
	while(( year.isalpha() and year!='all') or (year.isdigit() and (int(year)>2013 or int(year)<2002))):
		print("Invalid year")
		year=input("Enter a season (2002-2013)or type 'all' for all seaons => ")
		year=year.strip()
	print("-"*50)
	if year.isalpha() and year.lower()=='all':
		return 'all'
	return year

#checks if input is valid and if so calls corresponding function
def process_input(choice,team):
	if choice=="w":
		team_weather(team)
	elif choice=='t':
		team=team_input()
	elif choice=='d':
		hardest_season(team)
	elif choice=='p':
		playoffs_results(team)
	elif choice=='s':
		year=get_year()
		if year=='all':
			y=2002
			while y<=2013:
				season_stats(team,y)
				y+=1
		else:
			season_stats(team,year)
	elif choice=='b':
		
		SuperBowl(team)
	else:
		print("invalid input")
	
	return team
#asks user for a valid nfl team name and returns full name
def team_input():
	input_team=input("Enter the team name of an NFL team => ")
	input_team=input_team.strip()
	team=check_name(input_team.lower())
	while not team:
		print("Invalid team name")
		input_team=input("Enter the team name of an NFL team => ")
		input_team=input_team.strip()
		team=check_name(input_team.lower())
	return team

if __name__ == '__main__':
	team=team_input()
	print_menu(team)
	print("-"*50)
	choice=input("Choice? => ").strip().lower()
	print("-"*50)
	while(choice!='q'):
		team=process_input(choice,team)
		
		print_menu(team)
		print("-"*50)
		choice=input("Choice => ").strip().lower()
		print("-"*50)
		
	
	
	
	

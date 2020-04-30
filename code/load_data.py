import psycopg2

connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"

conn = psycopg2.connect(connection_string)

cursor = conn.cursor()


#dictionary of teams with 2-3 letter ids that are not the first 3 letters of their team name
#will make joining the 2 datasets easier
teams={"Green Bay Packers":"GB","St. Louis Cardinals":"STL","Boston Patriots":"NE","St. Louis Rams":"STL","Los Angeles Rams":"LA","New York Giants":"NYG","New York Jets":"NYJ","Los Angeles Cardinals":"LA", "San Francisco 49ers":"SF","Tampa Bay Buccaneers":"TB","Kansas City Chiefs":"KC","New England Patriots":"NE","New Orleans Saints":"NO","San Diego Chargers":"SD","Jacksonville Jaguars":"JAX"}

#replace all empty strings with null
def insert_null(l):
	for i in range(len(l)):
		if l[i]=="":
			l[i]="null"
#get 2-3 letter team id
def get_team_id(name):
	if name in teams:
		return teams[name]

	return name[0:3].upper()

def setUp():
	with conn.cursor() as cursor:
		with open('schema.sql', 'r') as setup:
			setup_queries = setup.read()
			cursor.execute(setup_queries)
		conn.commit()

def readStandings():
	with open("datasets/standings.csv",newline="") as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0

		for row in spamreader:
			#skip first row
			if i==0:
				i+=1
				continue
			#insert nulls to empty fields
			insert_null(row)

			query="INSERT INTO standings VALUES ("
			for j in range(len(row)):
				#varchar fields
				if (j>0 and j<4) or j==15:
					query+="'"+row[j]+"'"
				
				#numeric fields
				else:
					query+=row[j]

				if j!=len(row)-1:
					query+=", "
			query+=");"
			with conn.cursor() as cursor:
				cursor.execute(query)
			conn.commit()
		


def readGamesAndWeather():
	with open("datasets/weather_20131231.csv",newline="") as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		
		for row in spamreader:
			#skip first row
			if(i==0):
				i+=1
				print(row)
				continue

			weather_query="INSERT INTO Weather VALUES ("
			games_query="INSERT INTO Games VALUES ("
			#get 2-3 letter team ids
			homeid=get_team_id(row[1])
			awayid=get_team_id(row[3])
			row[7]=row[7][0:len(row[7])-1]
			#replace empty fields with null
			insert_null(row)
			for j in range(len(row)-1):
				#insert 2-3 letter team ids
				if j==2: 
					games_query+="'"+homeid+"', "
				elif j==4: 
					games_query+="'"+awayid+"', "

				#varchar fields
				if (j==0):#game id
					weather_query+="'"+row[j]+"', "
					games_query+="'"+row[j]+"', "
				elif(j==9):#weather summary
					weather_query+="'"+row[j]+"', "
				elif( j==1 or j==3 ): #team names
					games_query+="'"+row[j]+"', "

				#numeric fields
				elif(j==2 or j==4):#scores
					games_query+=row[j]+", "
				else: #weather data
					weather_query+=row[j]+", "
				
				
				
			#format date	
			date=row[10].split("/")
			weather_query+="'"+date[2]+'-'+date[0]+'-'+date[1]+"');"
			games_query+="'"+date[2]+'-'+date[0]+'-'+date[1]+"');"

			with conn.cursor() as cursor:
				cursor.execute(weather_query)
			conn.commit()
			with conn.cursor() as cursor:
				cursor.execute(games_query)
			conn.commit()

def main():
    # TODO invoke your code to load the data into the database
    print("Loading data")
    setUp()
    
   
    # Load data into Conferences table
    print("Inserting data into conference table")
    insert_query = "INSERT INTO Conference (name) VALUES (%(name)s)"
    cursor.execute(insert_query, dict(name="AFC"))
    cursor.execute(insert_query, dict(name="NFC"))
    print("Done inserting data into conference table")
    # Load data into Division table

    # Load data into Team table

    # Load data into Games and Weather table
    readGamesAndWeather()
 

    # Load data into Standings table
    readStandings()
    # Load data into Statistics table

    # Load data into Playoffs table


if __name__ == "__main__":
    main()

import psycopg2

connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"

conn = psycopg2.connect(connection_string)

cursor = conn.cursor()



def main():
    # TODO invoke your code to load the data into the database
    print("Loading data")
    # Load data into Conferences table
    print("Inserting data into conference table")
    insert_query = "INSERT INTO Conference (name) VALUES (%(name)s)"
    cursor.execute(insert_query, dict(name="AFC"))
    cursor.execute(insert_query, dict(name="NFC"))
    print("Done inserting data into conference table")
    # Load data into Division table

    # Load data into Team table

    # Load data into Game table

    # Load data into Weather table

    # Load data into Standings table

    # Load data into Statistics table

    # Load data into Playoffs table


if __name__ == "__main__":
    main()

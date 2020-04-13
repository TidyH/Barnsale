#Creates sqlite3 database and initializes a table and/or inserts pandas dataframe into one
#Garrett Waterman
#April 13 2020


import pandas as pd
import sqlite3 as sql
import path from os

#Check if database exists and create one if not
if os.path.exists("animals.db"):
    conn = sql.connect("animals.db")
    cursor =  conn.cursor()
else:
    conn = sql.connect("animals.db")
    cursor =  conn.cursor()
    #create a table
    cursor.execute("""CREATE TABLE animals
                      (id integer, date text, lot text, animal text, weight integer, Price real)
                   """)

#function for inserting data from pandas dataframe
def insert_query(dataframe):
    cursor.execute(dataframe)
    conn.commit()

#function for grabbing pickled pandas dataframe and formatting it for DB insert
def grab_pickle(pickle):
    df = pd.read_pickle(pickle)
    
    #turn file name into date column
    #Pickle should be passed in as filename string

    #get number of rows in dataframe
    count = len(df.index)

    #add date to all rows in dataframe at correct column pos
    date = [pickle] * count
    df.insert(0, "Date", pickle, True)
    

    #add uid to all rows in dataframe
    #find final entry to being uids for new entry
    cur.execute("SELECT max(id) from animals")
    n = cur.fetchone()[0]

    #add uid to table
    entry = []

    for _ in range(count):
        entry.append(n + 1)
        n += 1

    df.insert(0, "ID", entry, True)

    #convert $perhweight to real numbers (stripping leading $)

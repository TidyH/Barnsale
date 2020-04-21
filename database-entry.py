#!/usr/bin/env python3
#Creates sqlite3 database and initializes a table and/or inserts pandas dataframe into one
#Garrett Waterman
#April 13 2020
#D:/labs/barnsale

import pandas as pd
import sqlite3 as sql
import os.path
import sys

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
#def insert_query(dataframe):
#    cursor.execute(dataframe)
#    conn.commit()
#This was added to the end of the grab_pickle function

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
    cursor.execute("SELECT max(id) from animals")
    n = cursor.fetchone()[0]

    #add uid to table
    entry = []
    
    #check if n is None (generally will only happen when starting a new DB)
    if n is None:
        n = 0
    
    for _ in range(count):
        entry.append(n + 1)
        n += 1

    df.insert(0, "ID", entry, True)

    #convert $perhweight to real numbers (stripping leading $)
    update = pd.DataFrame({'$perhweight':[i[1:] for i in df['$perhweight']]})
    df.update(update)

    #insert data into database
    df.to_sql("animals", conn, if_exists="replace")

#run
#print(sys.argv[1])
args = sys.argv[1]
grab_pickle(args)

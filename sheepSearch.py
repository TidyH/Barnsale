#!/usr/bin/env python3

import sqlite3 as sql
import requests
import re
from bs4 import BeautifulSoup
from datetime import date
import os.path
import sys
import pandas as pd

#function that searches for new sheep postings and grabs them
def getSheep():

    url = "http://sfrlinc.com/web/previous-sales/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    linklist =[]

    #finds all links and formats them with just hyperlink and stores them in the linklist variable
    for link in soup.find_all('a'):
        linklist.append(link.get('href'))

    #save the list into history file to be rechecked when run
    if os.path.isfile('site_history'):
        file = open('site_history', 'r')
        file_listed = file.readlines()
    else:
        file = open('site_history', 'w')
        for link in linklist:
            file.write(link + "\n")
        file = open('site_history', 'r')
        file_listed = file.readlines()

    #check new entry to see if it has a match in the saved copy
    with open('site_history') as f:
        lines = f.read().splitlines()

    for link in linklist:
        if link not in lines:
            print(link)
            #If we have a new entry, we need to move to that web page and collect data
            url = link
            r = requests.get(url, headers=headers)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            tables = soup.select('table')[5]
            rows = tables.find_all('tr')
            output = []
            for row in rows:
                cols = row.find_all('td')
                cols = [item.text.strip() for item in cols]
                output.append([item for item in cols if item])
            df = pd.DataFrame(output, columns = ['Lot','Animal','hweight','$perhweight'])
            df = df.iloc[0:]
            #print(df)

            #append link to site_history
            file = open('site_history', 'a')
            file.write(link)

            return(df)

#debug make sure we are returning the dataframe
#print(getSheep())

def dbInput(dataFrame):
    #Check if database exists and create one if not
    if os.path.exists("animals.db"):
        conn = sql.connect("animals.db")
        cursor =  conn.cursor()
    else:
        conn = sql.connect("animals.db")
        cursor =  conn.cursor()
        #create a table
        print("is this false")
        cursor.execute("""CREATE TABLE animals
                      (id integer, date text, lot text, animal text, weight integer, Price real)
                       """)

    #rename to df for consistancy with previous function
    df = dataFrame

    #get number of rows in dataframe
    count = len(df.index)

    #add date to all rows in dataframe at correct column pos
    today = date.today()
    day = [today.strftime("%m-%d-%Y")] * count
    df.insert(0, "Date", day, True)

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
    df.to_sql("animals", conn, if_exists="append")


#Begin Main
def main():
    dbInput(getSheep())

if __name__ == "__main__":
    main()

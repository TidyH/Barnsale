import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import os.path
import pandas as pd

url = "http://sfrlinc.com/web/previous-sales/"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
data = r.text
soup = BeautifulSoup(data, 'html.parser')

#example code for listing all hyperlinks
#for link in soup.find_all('a'):
#    print(link.get('href'))


#alternate example code for listing links with regex
#for link in soup.find_all('a', href=re.compile('^http://sfrlinc.com/web/project/')):
#    print(link.get('href'))

#list to hold links
linklist = []

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
        print(df)



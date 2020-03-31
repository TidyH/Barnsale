import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import os.path

url = "http://sfrlinc.com/web/previous-sales/"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
data = r.text
soup = BeautifulSoup(data, 'html.parser')


#Find last record entered
#date = date.today()
#print(date)
date_month_check = datetime.today().strftime('%B')
date_day_check = datetime.today().strftime('%d')
#Debugging
#print(date_month_check)
#print(date_day_check)
#print('next check')

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

#Debugging
#print(linklist)
#print('next check')

#finds specific date hyperlink
#TODO: turn december-23 into a smart variable so it can run on its own
#Sheep sales happen every wednseday and are formated as MONTH-## or MONTH-##-## indicating a range of dates
#for links in linklist:
#    if 'december-23' in links:
#        print(links)

#checks date to see if their is a greater value
#matching_months = []
#for i in linklist:
#    if i.__contains__(date_month_check.lower()):
#        matching_months.append(i)
#print(matching_months)

#This gets me just march entries, but how do i figure out how to get a specific week?
#get last week's dates in a list and see if the links contain atleast one of them?
#another idea was to keep a list from the previous check and do a diff on what is new then overwrite the history
dif = []
#save the list into history file to be rechecked when run
if os.path.isfile('site_history'):
    file = open('site_history', 'r')
    file_listed = file.readlines()
#todo compare to lists and print the difference.
#    if file_listed != linklist:
#        diff = list(set(linklist) - set(file_listed))
#        print(diff)
else:
    file = open('site_history', 'w')
    for link in linklist:
        file.write(link + '\n')

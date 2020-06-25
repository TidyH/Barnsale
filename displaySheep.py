#!/usr/bin/env python3

import pandas as pd
import sqlite3 as sql
import plotly.express as px


#grab all data from database
pd.set_option('display.max_rows', 500)

conn = sql.connect("animals.db")
cur = conn.cursor()

animals_df = pd.read_sql_query("SELECT * from animals;", conn)

#convert lot column to int64
animals_df['Lot'] = pd.to_numeric(animals_df['Lot'])

#dataframe of lot totals by date
lot_df = animals_df.groupby('Date')['Lot'].sum().to_frame(name = 'lot_amount').reset_index()
#print(lot_df)

#create figure for a line graph
fig = px.bar(lot_df, x='Date', y='lot_amount')
fig.show()

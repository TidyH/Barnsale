#!/usr/bin/env python3
#Simple select all for testing database

import sqlite3 as sql
import pandas as pd

conn = sql.connect("animals.db")
cur = conn.cursor()

query = pd.read_sql_query("SELECT * from animals", conn)
print(query)

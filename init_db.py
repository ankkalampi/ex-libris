"""
This module initializes database for the application
"""

import sqlite3

FILE = "database.db"

try:
    connection = sqlite3.connect(FILE)
    cursor = connection.cursor()
except Exception as e:
    print(e)

with open('schema.sql', encoding='utf-8') as schema:
    schema_sql = schema.read()

cursor.executescript(schema_sql)

connection.commit()

with open('init.sql') as init:
    init_sql = init.read()

cursor.executescript(init_sql)

connection.commit()
connection.close()

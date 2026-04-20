import sqlite3

FILE = "database.db"

try:
    connection = sqlite3.connect(FILE)
    cursor = connection.cursor()
    print("database created")
except Exception as e:
    print("database creation failed")
    print(e)

with open('schema.sql') as schema:
    schema_sql = schema.read()
    

cursor.executescript(schema_sql)

connection.commit()
connection.close()

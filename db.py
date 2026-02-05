import sqlite3
from flask import g

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, connection, params=[]):
    result = connection.execute(sql, params)
    connection.commit()
    g.last_insert_id = result.lastrowid


def last_insert_id():
    return g.last_insert_id

def query(sql, connection, params=[]):
    result = connection.execute(sql, params).fetchall()
    return result

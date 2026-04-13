import sqlite3
from flask import g
from functools import wraps

class DBHandler:
    def __init__(self):
        self.connection = get_connection()
        self.cursor = connection.cursor

    def execute(self, sql, params=[]):
        result = self.cursor.execute(sql, params)
        g.last_insert_id = result.lastrowid

def modifies_db(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        handler = DBHandler()

        try:
            handler.connection.execute("BEGIN TRANSACTION;")

            f(*args, **kwargs)

            handler.connection.commit()

        except Exception as e:
            print(e)
            raise

        finally:
            connection.close()



def get_connection():
    """opens database connection"""
    connection = sqlite3.connect("database.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection

def execute(sql, params=[]):
    """executes sql query on database"""
    connection = get_connection()
    try:
        result = connection.execute(sql, params)
        connection.commit()
        g.last_insert_id = result.lastrowid
    finally:
        connection.close()


def last_insert_id():
    return g.last_insert_id

def query(sql, params=[]):
    """returns sql query result"""
    connection = get_connection()
    try:
        result = connection.execute(sql, params).fetchall()
        return result
    finally:
        connection.close()

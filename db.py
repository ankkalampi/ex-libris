import sqlite3
from flask import g
from functools import wraps
from enum import Enum


def get_connection():
    """opens database connection"""
    connection = sqlite3.connect("database.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection




                



def modifies_db(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        g.connection = get_connection()

        def db_execute(sql, params=[]):
            result = g.connection.cursor().execute(sql, params)
            g.last_insert_id = result.lastrowid
        
        
        g.db_execute = db_execute
        

        try:
            print("starting trying")
            g.connection.execute("BEGIN TRANSACTION;")

            print("begin transaction executed ")
            f(*args, **kwargs)

            print("decorated function successfully run")
            g.connection.commit()

        except Exception as e:
            print("EXCEPTION ENCOUNTERED")
            print(e)
            raise

        finally:
            g.connection.close()

    return decorated_function





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

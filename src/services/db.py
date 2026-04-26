from functools import wraps
import sqlite3
from flask import g

def get_connection():
    """opens database connection"""

    connection = sqlite3.connect("database.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection

def modify_db(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        g.connection = get_connection()

        def db_execute(sql, params=[]):
            result = g.connection.cursor().execute(sql, params)
            g.last_insert_id = result.lastrowid

        g.db_execute = db_execute

        try:
            g.connection.execute("BEGIN TRANSACTION;")
            f(*args, **kwargs)
            g.connection.commit()
        except Exception as e:
            print(e)
            raise
        finally:
            g.connection.close()

    return decorated_function

def query_db(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        g.connection = get_connection()

        def db_query(sql, params=[]):
            result = g.connection.execute(sql, params).fetchall()
            return result

        g.db_query = db_query

        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            raise
        finally:
            g.connection.close()

    return decorated_function

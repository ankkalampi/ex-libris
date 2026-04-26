"""
This module handles database operations for users.
"""

import sqlite3
from functools import wraps
from flask import redirect, session, url_for, g, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from src.services import db

def csrf_required(f):
    """Decorator function to check for CSRF token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.form["csrf_token"]:
            if request.form["csrf_token"] != session["csrf_token"]:
                abort(403)

        elif request.args["csrf_token"]:
            if request.args["csrf_token"] != session["csrd_token"]:
                abort(403)

        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    """Decorator function to check for login status"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('view.index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@db.query_db
def login(username, password):
    """
    Attempts to login user

    Args:
        username (str): username
        password (str): password
    """

    sql = "SELECT password_hash, id FROM users WHERE username = ?"
    result = g.db_query(sql, [username])

    if not result:
        session["login_message"] = "Käyttäjää ei löydy"
        return False

    password_hash = result[0][0]
    user_id = result[0][1]

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        return True
    else:
        session["login_message"] = "Väärä käyttäjätunnus tai salasana"
        return False

@db.modify_db
def create_user(username, password):
    """
    Attempts to register new user

    Args:
        username (str): username given
        password (str): password given
    """

    password_hash = generate_password_hash(password)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        g.db_execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        session["register_message"] = "VIRHE: tunnus on jo varattu"
        raise

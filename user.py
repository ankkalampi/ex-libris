import sqlite3
import db
from flask import redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

def get_user_id(username):
    """gets user db id based on username"""
    try:
	    sql = "SELECT id FROM users WHERE username = ?"
	    result = db.query(sql, [username])
	    user_id = result[0][0]
    except:
	    print(f"Database error in finding user id, user_id: {user_id} ")
	    return redirect("/")

    return user_id

def login(username, password):
    """attempts to login user"""
    sql = "SELECT password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if not result:
        session["login_message"] = "Käyttäjää ei löydy"
        return False

    password_hash = result[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return True
    else:
        session["login_message"] = "Väärä käyttäjätunnus tai salasana"
        return False

def create_user(username, password1, password2):
    """attempts to register new user"""
    

    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        session["register_message"] = "VIRHE: tunnus on jo varattu"
        return redirect("/register")
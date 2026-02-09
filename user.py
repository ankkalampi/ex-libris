import sqlite3
import db

def get_user_id(username):
    try:
	    sql = "SELECT id FROM users WHERE username = ?"
	    result = db.query(sql, [username])
	    user_id = result[0][0]
    except:
	    print(f"Database error in finding user id, user_id: {user_id} ")
	    return redirect("/")

    return user_id
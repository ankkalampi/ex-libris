import sqlite3
import db
import user
from flask import redirect

def get_shelves(username):
    """returns all bookshelves of a user"""
    

    try:
	    sql = """
        SELECT s.name, COUNT(sb.book_id), s.description, s.id 
        FROM shelves s
        JOIN users u ON u.id = s.user_id
        LEFT JOIN shelf_books sb ON s.id = sb.shelf_id
        WHERE u.username = ?
        GROUP BY s.name, s.description, s.id
        """
	    shelves = db.query(sql, [username])
    except Exception as e:
        print(f"Database error in selecting shelves")
        print(e)    
        raise

    return shelves

def get_shelf(shelf_name, username):
    """returns a shelf based on db id"""

    try:
        sql = """
        SELECT s.name, COUNT (sb.book_id), s.description
        FROM shelves s
        JOIN users u ON u.id = s.user_id
        LEFT JOIN shelf_books sb ON s.id = sb.shelf_id 
        WHERE s.name = ? AND u.username = ?
        """
        shelf = db.query(sql, [shelf_name, username])
    except Exception as e:
        print("Database error in fetching shelf")
        print(e)
        raise

    return shelf

def create_shelf(username, name, description, public):
    """creates new bookshelf"""
    user_id = user.get_user_id(username)

    try:
	    sql = "INSERT INTO shelves (user_id, name, description, public) VALUES (?, ?, ?, ?)"
	    db.execute(sql, [user_id, name, description, public])
    except Exception as e:
        print(e)
        print("Database error in creating new shelf")
        raise

def delete_shelf(shelf_id):
    """deletes a bookshelf based on db id"""

    try:
        sql = "DELETE FROM shelves WHERE id = ?"
        db.execute(sql, [shelf_id])
    except Exception as e:
        print(e)
        print("Database error in deleting shelf")
        raise







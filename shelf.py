import sqlite3
import db
import user
from flask import redirect

def get_shelves(username):
    """returns all bookshelves of a user"""
    
    user_id = user.get_user_id(username)

    try:
	    sql = "SELECT name, number_of_books, description, id FROM shelves WHERE user_id = ?"
	    shelves = db.query(sql, [user_id])
    except:
	    print(f"Database error in selecting shelves, user_id: {user_id}")
	    return redirect("/")

    return shelves

def get_shelf(shelf_id):
    """returns a shelf based on db id"""

    try:
        sql = "SELECT name, number_of_books, description FROM shelves WHERE id = ?"
        shelf = db.query(sql, [shelf_id])
    except:
        print("Database error in fetching shelf")
        return redirect("/")

    return shelf


def create_self(username, name, description):
    """creates new bookshelf"""
    user_id = user.get_user_id(username)

    try:
	    sql = "INSERT INTO shelves (user_id, name, number_of_books, description) VALUES (?, ?, ?, ?)"
	    db.execute(sql, [user_id, name, 0, description])
    except:
	    print("Database error in creating new shelf")
	    return redirect ("/")

def delete_shelf(shelf_id):
    """deletes a bookshelf based on db id"""

    try:
        sql = "DELETE FROM shelves WHERE id = ?"
        db.execute(sql, [shelf_id])
    except:
        print("Database error in deleting shelf")
        return redirect ("/")





def get_books(shelf):
    pass

def add_book(book, shelf):
    pass

def remove_book(book, shelf):
    pass


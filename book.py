import sqlite3
import db
import user
from flask import redirect, g, session


def create_book(username, shelf_id, name, author, pages, synopsis): 
    """creates a book onto db"""
    user_id = user.get_user_id(username)

    connection = db.get_connection()

    try:
        connection.execute("BEGIN TRANSACTION;")

        sql_insert_to_books = """
        INSERT INTO books (name, author, pages, synopsis, user_id)
        VALUES (?, ?, ?, ?, ?);
        """
        result = connection.execute(
            sql_insert_to_books,
            [
                name,
                author,
                pages,
                synopsis,
                user_id
            ]
        )

        g.last_insert_id = result.lastrowid        
        book_id = g.last_insert_id

        sql_insert_to_user_books = """
        INSERT INTO user_books (user_id, book_id)
        VALUES (?, ?);
        """
        connection.execute(
            sql_insert_to_user_books,
            [
                user_id,
                book_id
            ]
        )

        sql_insert_to_shelf_books = """
        INSERT INTO shelf_books (shelf_id, book_id)
        VALUES (?, ?);
        """
        connection.execute(
            sql_insert_to_shelf_books,
            [
                shelf_id,
                book_id
            ]
        )

        connection.commit()
        

    except sqlite3.IntegrityError:
        session["add_book_message"] = "VIRHE: Kirja on jo olemassa"
        return redirect(f"/{username}/{shelf_id}/uusi-kirja")

    finally:
        connection.close()
    



def get_books(shelf_id):
    """returns all books in a shelf"""

def check_if_book_exists(name, author, username):
    """checks if a user has already added a book. Returns """
    


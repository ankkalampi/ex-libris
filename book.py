import sqlite3
import db
import user
from flask import redirect, g, session
import shelf


def create_book(username, shelf_name, name, author, pages, synopsis): 
    """creates a book onto db"""
    user_id = user.get_user_id(username)
    shelf_id = shelf.get_shelf_id(shelf_name)

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
        raise

    finally:
        connection.close()
    



def get_books(shelf_id):
    """returns all books in a shelf"""

    print(f"SHELF ID: {shelf_id}")
    try:
        sql = """
        SELECT id, name, author, pages, synopsis 
        FROM books
        JOIN shelf_books ON books.id = shelf_books.book_id
        WHERE shelf_books.shelf_id = ?
        """
        books = db.query(sql, [shelf_id])
        
    except Exception as e:
        print(e)
        shelf_name = shelf.get_shelf_name(shelf_id)
        print(f"SHELF NAME: {shelf_name}")
        return redirect(f"/")

    return books

def search(name, author, public):
    pass
    

    


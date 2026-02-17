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
        return redirect(url_for("shelf_view"))
    
    

    return books

def search(name, author, public, username):
    try:
        if (public == 1):
            sql = """
            SELECT b.name, b.author, b.pages, b.synopsis, u.username, s.name
            FROM books b
            JOIN user_books ub ON b.id = ub.book_id
            JOIN users u ON ub.user_id = u.id
            JOIN shelf_books sb ON b.id = sb.book_id
            JOIN shelves s ON sb.shelf_id = s.id
            WHERE (u.username = ? OR s.public = 1)
            AND (b.name = ? AND b.author = ?)
            """
            result = db.query(sql, [username, "%"+name+"%", "%"+author+"%"])

        else:
            sql = """
            SELECT b.name, b.author, b.pages, b.synopsis, u.username, s.name
            FROM books b
            JOIN user_books ub ON b.id = ub.book_id
            JOIN users u ON ub.user_id = u.id
            JOIN shelf_books sb ON b.id = sb.book_id
            JOIN shelves s ON sb.shelf_id = s.id
            WHERE u.username = ?
            AND (b.name = ? AND b.author = ?)
            """
            result = db.query(sql, [username, "%"+name+"%", "%"+author+"%"])

    except Exception as e:
        print(e)
        return redirect(url_for("search"))

    return result
    

    


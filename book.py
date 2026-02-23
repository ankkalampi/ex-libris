import sqlite3
import db
import user
from flask import redirect, g, session, url_for
import shelf


def create_book(username, shelf_name, name, author, pages, year, ISBN, synopsis): 
    """creates a book onto db"""

    connection = db.get_connection()

    try:
        connection.execute("BEGIN TRANSACTION;")

        sql_insert_to_books = """
        INSERT INTO books (name, author, pages, year, ISBN, synopsis, user_id)
        VALUES (?, ?, ?, ?, ?, ?, (SELECT id FROM users WHERE username = ? ));
        """
        result = connection.execute(
            sql_insert_to_books,
            [
                name,
                author,
                pages,
                year,
                ISBN,
                synopsis,
                username
            ]
        )

        g.last_insert_id = result.lastrowid        
        book_id = g.last_insert_id

        sql_insert_to_user_books = """
        INSERT INTO user_books (user_id, book_id)
        VALUES ((SELECT id FROM users WHERE username = ? ), ?);
        """
        connection.execute(
            sql_insert_to_user_books,
            [
                username,
                book_id
            ]
        )

        sql_insert_to_shelf_books = """
        INSERT INTO shelf_books (shelf_id, book_id)
        VALUES ((SELECT id FROM shelves WHERE name = ? ), ?);
        """
        connection.execute(
            sql_insert_to_shelf_books,
            [
                shelf_name,
                book_id
            ]
        )

        connection.commit()
        

    except sqlite3.IntegrityError:
        raise

    finally:
        connection.close()
    



def get_books(shelf_name, username):
    """returns all books in a shelf belonging to a user"""

    
    try:
        sql = """
        SELECT b.id, b.name, b.author, b.year, b.ISBN, b.pages, b.synopsis 
        FROM books b
        JOIN shelf_books sb ON b.id = sb.book_id
        JOIN shelves s ON sb.shelf_id = s.id
        JOIN users u ON s.user_id = u.id
        WHERE s.name = ? AND u.username = ?
        """
        books = db.query(sql, [shelf_name, username])

    
        
    except Exception as e:
        print(e)
        return redirect(url_for("shelf_view", shelf_name=shelf_name, username=username))
    
    

    return books

def search(name, author, year, isbn, public, username):
    try:
        if (public == 1):
            sql = """
            SELECT b.name, b.author, b.pages, b.year, b.synopsis, b.ISBN, u.username, s.name
            FROM books b
            JOIN user_books ub ON b.id = ub.book_id
            JOIN users u ON ub.user_id = u.id
            JOIN shelf_books sb ON b.id = sb.book_id
            JOIN shelves s ON sb.shelf_id = s.id
            WHERE (u.username = ? OR s.public = 1)
            AND (b.name LIKE ? AND b.author LIKE ? AND b.year = LIKE ? AND b.ISBN LIKE ?)
            """
            result = db.query(sql, [username, "%"+name+"%", "%"+author+"%", "%"+year+"%", "%"+isbn+"%"])

        else:
            sql = """
            SELECT b.name, b.author, b.pages, b.year, b.synopsis, b.ISBN, u.username, s.name
            FROM books b
            JOIN user_books ub ON b.id = ub.book_id
            JOIN users u ON ub.user_id = u.id
            JOIN shelf_books sb ON b.id = sb.book_id
            JOIN shelves s ON sb.shelf_id = s.id
            WHERE u.username = ?
            AND (b.name LIKE ? AND b.author LIKE ? AND b.year LIKE ? AND b.ISBN LIKE ?)
            """
            result = db.query(sql, [username, "%"+name+"%", "%"+author+"%", "%"+year+"%", "%"+isbn+"%"])

    except Exception as e:
        print(e)
        return redirect(url_for("search"))

    return result
    

    


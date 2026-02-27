import sqlite3
import db
import user
from flask import redirect, g, session, url_for
import shelf


def create_book(username, shelf_name, name, author, pages, year, ISBN, synopsis): 
    """
    Creates a book onto db
    
    Args:
        username (str): Username of the user creating the book
        name (str): Name of the book 
        author (str): Name of the author 
        pages (int): Number of pages
        year (str): Publishing year
        ISBN (str): ISBN code
        synopsis (str): synopsis 
    """

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


def remove_book(book_id):

    connection = db.get_connection()

    try:
        connection.execute("BEGIN TRANSACTION")

        sql_delete_from_books = """
        DELETE FROM books WHERE id = ?
        """

        sql_delete_from_user_books = """
        DELETE FROM user_books WHERE book_id = ?
        """

        sql_delete_from_shelf_books = """
        DELETE FROM shelf_books WHERE book_id = ?
        """

        connection.execute(sql_delete_from_user_books, book_id)
        connection.execute(sql_delete_from_shelf_books, book_id)
        connection.execute(sql_delete_from_books, book_id)
        

        connection.commit()

    except Exception as e:
        print(e)
        raise

    finally:
        connection.close()




def get_books(shelf_name, username):
    """
    Returns all books in a shelf belonging to a user
    
    Args:
        shelf_name (str): Name of the shelf
        username (str): Username of the user

    Returns:
        List[Tuple(int, str, str, str, str, int, str)]: List of book information tuples in the form of 
            (book id,
            book name,
            book author,
            publishing year,
            ISBN,
            number of pages,
            synopsis)
    """

    
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
    """
    Constructs sql query for search and returns information on books searched.

    Args:
        name (str): Name of the searched book
        author (str): Author of the searched book
        year (str): Publishing year of the searched book
        isbn (str): ISBN of the searched book
        public (int): Toggle search from all public shelves (can be 0 or 1)
        username (str): The current user sarching

    Returns:
        List[Tuple(str, str, int, str, str, str, str, str)]: List of book information tuples in the form of 
            (book name, 
            book author,
            number of pages, 
            publishing year, 
            synopsis, ISBN, 
            owner username, 
            shelf name)
    """
    try:

        sql_begin = """
            SELECT b.name, b.author, b.pages, b.year, b.synopsis, b.ISBN, u.username, s.name
            FROM books b
            JOIN user_books ub ON b.id = ub.book_id
            JOIN users u ON ub.user_id = u.id
            JOIN shelf_books sb ON b.id = sb.book_id
            JOIN shelves s ON sb.shelf_id = s.id
            """

        if (public ==1):
            sql_middle = """
            WHERE (u.username = ? OR s.public = 1)
            """
        else:
            sql_middle = """
            WHERE u.username = ?
            """

        if isbn:
            sql = sql_begin + sql_middle + """
            AND (b.name LIKE ? AND b.author LIKE ? AND b.year LIKE ? AND b.ISBN LIKE ?)
            """
            params = [
                username,
                "%"+name+"%",
                "%"+author+"%",
                "%"+year+"%",
                "%"+isbn+"%"
                ]
            
        else:
            sql = sql_begin + sql_middle + """
            AND (b.name LIKE ? AND b.author LIKE ? AND b.year LIKE ?)
            """

            params = [
                username,
                "%"+name+"%",
                "%"+author+"%",
                "%"+year+"%"
                ]
            

        result = db.query(sql, params)
        
        
        
    except Exception as e:
        print(e)
        return redirect(url_for("search"))

    return result
    

    


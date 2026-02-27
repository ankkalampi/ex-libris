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

def modify_book(username, shelf_name, book_id, name, author, year, synopsis, ISBN, pages, ):
    """
    Modifies book data of a single book

    Args:
        username (str): username for redirection
        shelf_name (str): shelf name for redirection
        book_id (int): id of the book being modified
        name (str): new name for the book
        author (str): new author for the book
        year (str): new publishing year for the book
        synopsis (str): new synopsis for the book
        ISBN (str): new ISBN for the book
        pages (int): new number of pages for the book 
    """
    connection = db.get_connection()


    number_of_args = 1
    arg_list = []

    sql_final = "UPDATE books SET "

    if (name):
        sql_final += "name = ?, "
        number_of_args += 1
        arg_list.append(name)
    if(author):
        sql_final += "author = ?, "
        number_of_args += 1
        arg_list.append(author)
    if(year):
        sql_final += "year = ?, "
        number_of_args += 1
        arg_list.append(year)
    if(synopsis):
        sql_final += "synopsis = ?, "
        number_of_args += 1
        arg_list.append(synopsis)
    if(ISBN):
        sql_final += "ISBN = ?, "
        number_of_args += 1
        arg_list.append(ISBN)
    if(pages):
        sql_final += "pages = ?, "
        number_of_args += 1
        arg_list.append(pages)

    sql_final = sql_final[:-2]
    sql_final += " "
    sql_final += "WHERE id = ?"
    arg_list.append(book_id)
    
    if (number_of_args == 1):
        session["book_modification_message"] = "jokin kenttä täytettävä"
        return redirect(url_for("modify_book_view", username=username, book_id=book_id, shelf_name=shelf_name))

    try:
        connection.execute(sql_final, arg_list)
        connection.commit()

    except Exception as e:
        print(e)
        print(sql_final)
        raise

    finally:
        connection.close()

        

        

        

def remove_book(book_id):
    """
    Removes a book from db based on unique id

    Args:
        book_id (int): unique id of book to be removed
    """

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

def get_book(book_id):
    """
    Get info of a single book bsed on book id

    Args:
        book_id (int): id of the book

    Returns:
        Tuple(int, str, str, str, str, int, str): Tuple of book information in the form of 
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
        SELECT id, name, author, year, ISBN, pages, synopsis
        FROM books
        WHERE id = ? 
        """
        book = db.query(sql, [book_id])[0]
        

    except Exception as e:
        print(e)
        raise

    return book






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
    

    


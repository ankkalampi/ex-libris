from flask import g
import services.db as db
import services.user as user
import services.shelf as shelf

class BookModificationFieldsEmpty(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

@db.modify_db
def create_book(user_id, shelf_name, name, author, pages, year, ISBN, synopsis): 
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

    sql_insert_to_books = """
    INSERT INTO books (name, author, pages, year, ISBN, synopsis, user_id)
    VALUES (?, ?, ?, ?, ?, ?, (SELECT id FROM users WHERE id = ? ));
    """
    params_insert_to_books = [
        name,
        author,
        pages,
        year,
        ISBN,
        synopsis,
        user_id
        ]

    g.db_execute(sql_insert_to_books, params_insert_to_books)
    
      
    book_id = db.last_insert_id()

    sql_insert_to_user_books = """
    INSERT INTO user_books (user_id, book_id)
    VALUES ((SELECT id FROM users WHERE id = ? ), ?);
    """
    params_insert_to_user_books = [
        user_id,
        book_id
        ]

    g.db_execute(sql_insert_to_user_books, params_insert_to_user_books)

    sql_insert_to_shelf_books = """
    INSERT INTO shelf_books (shelf_id, book_id)
    VALUES ((SELECT id FROM shelves WHERE name = ? ), ?);
    """
    params_insert_to_shelf_books = [
        shelf_name,
        book_id
        ]
    
    g.db_execute(sql_insert_to_shelf_books, params_insert_to_shelf_books)

@db.modify_db
def modify_book(user_id, shelf_name, book_id, name, author, year, synopsis, ISBN, pages):
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
        raise BookModificationFieldsEmpty("jokin kenttä täytettävä")

    g.db_execute(sql_final, arg_list)
        
@db.modify_db
def remove_book(book_id):
    """
    Removes a book from db based on unique id

    Args:
        book_id (int): unique id of book to be removed
    """

    sql_delete_from_books = """
    DELETE FROM books WHERE id = ?
    """

    sql_delete_from_user_books = """
    DELETE FROM user_books WHERE book_id = ?
    """

    sql_delete_from_shelf_books = """
    DELETE FROM shelf_books WHERE book_id = ?
    """

    g.db_execute(sql_delete_from_shelf_books, book_id)
    g.db_execute(sql_delete_from_user_books, book_id)
    g.db_execute(sql_delete_from_books, book_id)
    
@db.query_db
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

    sql = """
    SELECT id, name, author, year, ISBN, pages, synopsis
    FROM books
    WHERE id = ? 
    """
    
    return g.db_query(sql, [book_id])[0]
        
@db.query_db
def get_books(shelf_name, user_id):
    """
    Returns all books in a shelf belonging to a user
    
    Args:
        shelf_name (str): Name of the shelf
        user_id (int): id of the user

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

    sql = """
    SELECT b.id, b.name, b.author, b.year, b.ISBN, b.pages, b.synopsis 
    FROM books b
    JOIN shelf_books sb ON b.id = sb.book_id
    JOIN shelves s ON sb.shelf_id = s.id
    JOIN users u ON s.user_id = u.id
    WHERE s.name = ? AND u.id = ?
    """

    return g.db_query(sql, [shelf_name, user_id])

@db.query_db
def search(name, author, year, isbn, public, user_id):
    """
    Constructs sql query for search and returns information on books searched.

    Args:
        name (str): Name of the searched book
        author (str): Author of the searched book
        year (str): Publishing year of the searched book
        isbn (str): ISBN of the searched book
        public (int): Toggle search from all public shelves (can be 0 or 1)
        user_id (int): Id of the current user sarching

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
        WHERE (u.id = ? OR s.public = 1)
        """
    else:
        sql_middle = """
        WHERE u.id = ?
        """

    if isbn:
        sql = sql_begin + sql_middle + """
        AND (b.name LIKE ? AND b.author LIKE ? AND b.year LIKE ? AND b.ISBN LIKE ?)
        """
        params = [
            user_id,
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
            user_id,
            "%"+name+"%",
            "%"+author+"%",
            "%"+year+"%"
            ]
        
    return g.db_query(sql, params)
        
        
    
    

    


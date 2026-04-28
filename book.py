"""
This module handles database operations for books.
"""

from flask import g
import db

class BookModificationFieldsEmpty(Exception):
    """Exception class for empty book modification fields"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

@db.modify_db
def create_book(user_id, shelf_name, name, author, pages, year, ISBN, synopsis, tag_id):
    """
    Creates a book onto db

    Args:
        username (str): Username of the user creating the book
        shelf_id (name): name of the shelf where the book is being added
        name (str): Name of the book
        author (str): Name of the author
        pages (int): Number of pages
        year (str): Publishing year
        ISBN (str): ISBN code
        synopsis (str): synopsis
        tag_id (int): id of the tag that the book has
    """

    sql_insert_to_books = """
    INSERT INTO books (name, shelf_id, author, pages, year, ISBN, synopsis, tag_id, user_id)
    VALUES (?, (SELECT id FROM shelves WHERE name = ? AND user_id = ?), ?, ?, ?, ?, ?, ?, ?);
    """
    params_insert_to_books = [
        name,
        shelf_name,
        user_id,
        author,
        pages,
        year,
        ISBN,
        synopsis,
        tag_id,
        user_id
    ]

    g.db_execute(sql_insert_to_books, params_insert_to_books)

@db.modify_db
def modify_book(book_id, name, author, year, synopsis, ISBN, pages, tag_id):
    """
    Modifies book data of a single book

    Args:
        book_id (int): id of the book being modified
        name (str): new name for the book
        author (str): new author for the book
        year (str): new publishing year for the book
        synopsis (str): new synopsis for the book
        ISBN (str): new ISBN for the book
        pages (int): new number of pages for the book
        tag_id (int): new tag for the book
    """

    number_of_args = 1
    arg_list = []

    sql_final = "UPDATE books SET "

    if name:
        sql_final += "name = ?, "
        number_of_args += 1
        arg_list.append(name)
    if author:
        sql_final += "author = ?, "
        number_of_args += 1
        arg_list.append(author)
    if year:
        sql_final += "year = ?, "
        number_of_args += 1
        arg_list.append(year)
    if synopsis:
        sql_final += "synopsis = ?, "
        number_of_args += 1
        arg_list.append(synopsis)
    if ISBN:
        sql_final += "ISBN = ?, "
        number_of_args += 1
        arg_list.append(ISBN)
    if pages:
        sql_final += "pages = ?, "
        number_of_args += 1
        arg_list.append(pages)
    if tag_id:
        sql_final += "tag_id = ?, "
        arg_list.append(tag_id)

    sql_final = sql_final[:-2]
    sql_final += " "
    sql_final += "WHERE id = ?"
    arg_list.append(book_id)

    if number_of_args == 1:
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

    book_id = int(book_id)
    g.db_execute(sql_delete_from_books, [book_id])

@db.query_db
def get_book(book_id):
    """
    Get info of a single book based on book id

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
            synopsis,
            tag_id)
    """

    sql = """
    SELECT id, name, author, year, ISBN, pages, synopsis, tag_id
    FROM books
    WHERE id = ?
    """

    return g.db_query(sql, [book_id])[0]

@db.query_db
def get_books(shelf_name, user_id, page, page_size):
    """
    Returns all books in a shelf belonging to a user

    Args:
        shelf_name (str): Name of the shelf
        user_id (int): id of the user

    Returns:
        List[Tuple(int, str, str, str, str, int, str)]:
        List of book information tuples in the form of
            (book id,
            book name,
            book author,
            publishing year,
            ISBN,
            number of pages,
            synopsis,
            tag_id)
    """

    sql = """
    SELECT b.id, b.name, b.author, b.year, b.ISBN, b.pages, b.synopsis, t.name
    FROM books b
    JOIN tags t ON b.tag_id = t.id
    JOIN shelves s ON b.shelf_id = s.id
    WHERE s.name = ? AND b.user_id = ?
    LIMIT ? OFFSET ?
    """

    limit = page_size
    offset = limit * (page-1)

    return g.db_query(sql,
                      [shelf_name,
                       user_id,
                       limit,
                       offset])

@db.query_db
def get_number_of_shelf_books(user_id, shelf_name):
    """
    Returns number of books that a shelf has

    Args:
        user_id (int): Id of user

    Returns:
        int
    """

    sql = """
    SELECT COUNT(*)
    FROM books b
    JOIN shelves s ON b.shelf_id = s.id
    WHERE b.user_id = ? AND s.name = ?
    """

    result = g.db_query(sql, [user_id, shelf_name])[0][0]

    return result

@db.query_db
def get_number_of_all_books(user_id):
    """
    Returns number of books that a user has

    Args:
        user_id (int): Id of user

    Returns:
        int
    """

    sql = """
    SELECT COUNT(*)
    FROM books
    WHERE user_id = ?
    """

    result = g.db_query(sql, [user_id])[0][0]

    return result

@db.query_db
def get_search_length(name, author, year, isbn, public, user_id, tag_id):
    """
    Finds the length of a search query for paging

    Args:
        name (str): Name of the searched book
        author (str): Author of the searched book
        year (str): Publishing year of the searched book
        isbn (str): ISBN of the searched book
        public (int): Toggle search from all public shelves (can be 0 or 1)
        user_id (int): Id of the current user sarching
        tag_id (int): Id of the tag of the searched book

    Returns:
        List[Tuple(str, str, int, str, str, str, str, str, int)]:
            List of book information tuples in the form of
            (book name,
            book author,
            number of pages,
            publishing year,
            synopsis, ISBN,
            owner username,
            shelf name,
            tag id)
    """

    sql_begin = """
        SELECT COUNT(b.id)
        FROM books b
        JOIN users u ON u.id = b.user_id
        JOIN shelves s ON b.shelf_id = s.id
        JOIN tags t ON b.tag_id = t.id
        """

    if public == 1:
        sql_middle = """
        WHERE (b.user_id = ? OR s.public = 1)
        """
    else:
        sql_middle = """
        WHERE b.user_id = ?
        """

    sql_end = """
    AND (b.name LIKE ? AND b.author LIKE ? AND b.year LIKE ?
    """

    params = [
        user_id,
        "%"+name+"%",
        "%"+author+"%",
        "%"+year+"%"
    ]

    if tag_id:
        sql_end = sql_end + " AND b.tag_id = ? "
        params.append(tag_id)

    if isbn:
        sql_end = sql_end + " AND b.ISBN LIKE ? "
        params.append("%"+isbn+"%")

    sql = sql_begin + sql_middle + sql_end + " )"

    return g.db_query(sql, params)[0][0]

@db.query_db
def search(name, author, year, isbn, public, user_id, tag_id, page, page_size):
    """
    Constructs sql query for search and returns information on books searched.

    Args:
        name (str): Name of the searched book
        author (str): Author of the searched book
        year (str): Publishing year of the searched book
        isbn (str): ISBN of the searched book
        public (int): Toggle search from all public shelves (can be 0 or 1)
        user_id (int): Id of the current user sarching
        tag_id (int): Id of the tag of the searched book

    Returns:
        List[Tuple(str, str, int, str, str, str, str, str, int)]:
            List of book information tuples in the form of
            (book name,
            book author,
            number of pages,
            publishing year,
            synopsis, ISBN,
            owner username,
            shelf name,
            tag id)
    """

    limit = page_size
    offset = limit * (page-1)

    sql_begin = """
        SELECT b.name, b.author, b.pages, b.year, b.synopsis, b.ISBN, u.username, s.name, t.name
        FROM books b
        JOIN users u ON u.id = b.user_id
        JOIN shelves s ON b.shelf_id = s.id
        JOIN tags t ON b.tag_id = t.id
        """
    if public == 1:
        sql_middle = """
        WHERE (b.user_id = ? OR s.public = 1)
        """
    else:
        sql_middle = """
        WHERE b.user_id = ?
        """

    sql_end = """
    AND (b.name LIKE ? AND b.author LIKE ? AND b.year LIKE ?
    """

    params = [
        user_id,
        "%"+name+"%",
        "%"+author+"%",
        "%"+year+"%"
    ]

    if tag_id:
        sql_end = sql_end + " AND b.tag_id = ? "
        params.append(tag_id)

    if isbn:
        sql_end = sql_end + " AND b.ISBN LIKE ? "
        params.append("%"+isbn+"%")

    params.append(int(limit))
    params.append(int(offset))

    sql = sql_begin + sql_middle + sql_end + " ) LIMIT ? OFFSET ? "

    return g.db_query(sql, params)

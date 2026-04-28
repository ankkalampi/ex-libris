"""
This module handles database operations for shelves.
"""

from flask import g
import db

@db.query_db
def get_shelves(user_id, page, page_size):
    """
    Returns all bookshelves of a user

    Args:
        user_id (int): Id of the user
        page (int): variable for paging
        page_size (int): variable for paging
    """

    sql = """
    SELECT s.name, COUNT(b.id), s.description, s.id
    FROM shelves s
    LEFT JOIN books b ON s.id = b.shelf_id
    WHERE s.user_id = ?
    GROUP BY s.name, s.description, s.id
    LIMIT ? OFFSET ?
    """

    limit = page_size
    offset = page_size * (page-1)

    return g.db_query(sql, [user_id, limit, offset])

@db.query_db
def get_shelf(shelf_name, user_id):
    """
    Returns a shelf based on id

    Args:
        shelf_name (str): name of the shelf
        user_id (int): Id of the current users
    """

    sql = """
    SELECT s.name, COUNT (b.id), s.description, s.id
    FROM shelves s
    JOIN books b ON b.shelf_id = s.id
    WHERE s.name = ? AND s.user_id = ?
    """

    return g.db_query(sql, [shelf_name, user_id])

@db.query_db
def get_number_of_all_shelves(user_id):
    """
    Returns number of all shelves that a user has

    Args:
        user_id (int): Id of the user

    Returns:
        int
    """

    sql = """
    SELECT COUNT(id)
    FROM shelves
    WHERE user_id = ?
    """

    result = g.db_query(sql, [user_id])[0][0]

    return result

@db.modify_db
def create_shelf(user_id, name, description, public):
    """
    Creates new bookshelf

    Args:
        user_id (int): Id of the current user
        name (str): name of the shelf
        description (str): description of the shelf
        public (int): indicates if the shelf is public. Must be either 1 or 0

    """

    sql = "INSERT INTO shelves (user_id, name, description, public) VALUES (?, ?, ?, ?)"
    g.db_execute(sql, [user_id, name, description, public])

@db.modify_db
def delete_shelf(shelf_id):
    """
    Deletes a bookshelf

    Args:
        shelf_id (int): Id of the shelf
    """

    sql = "DELETE FROM shelves WHERE id = ?"

    g.db_execute(sql, [shelf_id])

from flask import g
import src.services.db as db


@db.query_db
def get_shelves(user_id):
    """returns all bookshelves of a user"""
    
    sql = """
    SELECT s.name, COUNT(sb.book_id), s.description, s.id 
    FROM shelves s
    JOIN users u ON u.id = s.user_id
    LEFT JOIN shelf_books sb ON s.id = sb.shelf_id
    WHERE u.id = ?
    GROUP BY s.name, s.description, s.id
    """

    return g.db_query(sql, [user_id])

@db.query_db
def get_shelf(shelf_name, user_id):
    """returns a shelf based on db id"""

    sql = """
    SELECT s.name, COUNT (sb.book_id), s.description
    FROM shelves s
    JOIN users u ON u.id = s.user_id
    LEFT JOIN shelf_books sb ON s.id = sb.shelf_id 
    WHERE s.name = ? AND u.id = ?
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
    """creates new bookshelf"""
    
    sql = "INSERT INTO shelves (user_id, name, description, public) VALUES (?, ?, ?, ?)"
    g.db_execute(sql, [user_id, name, description, public])
    
@db.modify_db
def delete_shelf(shelf_id):
    """deletes a bookshelf based on db id"""

    sql = "DELETE FROM shelves WHERE id = ?"
    g.db_execute(sql, [shelf_id])
    







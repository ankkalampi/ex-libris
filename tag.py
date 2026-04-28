"""
This module handles database operations for tags.
"""

from flask import g
import db

@db.query_db
def get_tag(tag_id):
    """
    Gets a single tag name based on its id

    Args:
        tag_id (int): Id of the tag
    """

    sql = """
    SELECT name
    FROM tags
    WHERE tag_id = ?
    """

    params = [tag_id]

    g.db_execute(sql, params)

@db.query_db
def get_all_tags():
    """
    Returns all tag names as a list

    Returns:
        List[str]: List of tag names
    """

    sql = """
    SELECT name
    FROM tags
    """

    return g.db_query(sql, [])

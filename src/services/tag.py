from flask import g
import services.db
import services.user as user

@db.modify_db
def create_tag(user_id, name):
    """
    Creates a new tag onto db. Name cannot be same as user's other tags or global tags.

    Args:
        user_id (int): User id of the tag owner
        name (str): Tag name
    """

    sql = """
    INSERT INTO tags (name, user_id)
    VALUES (?, ?)
    """

    params = [name, user_id]

    g.db_execute(sql, params)

@db.modify_db
def create_global_tag(name):
    """
    Creates a global tag onto db. Global tags have NULL as user_id value. Cannot be same as other global tags.

    Args:
        name (str): Tag name
    """
    
    sql = """
    INSERT INTO tags (name, user_id)
    VALUES (?, ?)
    """

    params = [name, NULL]

    g.db_execute(sql, params)

@db.modify_db
def remove_tag(tag_id):
    """
    Deletes user tag from db and deattaches it from all user books.

    Args:
        tag_id (int): Id of the tag
    """
    
    sql_delete_from_tags = """
    DELETE FROM tags WHERE id = ?
    """

    sql_delete_from_book_tags = """
    DELETE FROM book_tags WHERE tag_id = ?
    """

    params = [tag_id]

    g.db_execute(sql_delete_from_book_tags, params)
    g.db_execute(sql_delete_fromtags, params)
    

@db.query_db
def get_user_tags(user_id):
    """
    Returns a list of all the tags (except global ones) of a user.

    Args:
        user_id (int): Id of the user

    Returns:
        List[Tuple(str)]: List of tag names as single value tuples
    """
    
    sql = """
    SELECT id, name
    FROM tags
    WHERE user_id = ?
    """

    params = [user_id]

    return g.db_query(sql, params)

@db.query_db
def get_global_tags():
    """
    Returns a list of all global tags.

    Returns:
        List[Tuple(str)]: List of tag names as single value tuples
    """
    
    sql = """
    SELECT id, name
    FROM tags
    WHERE iser_id = ?
    """

    params = [NULL]

    return g.db_query(sql, params)

@db.modify_db
def attach_tag(tag_id, book_id):
    """
    Attaches a tag onto a book.

    Args:
        tag_id (int): Id of the tag
        book_id (int): Id of the book
    """
    
    sql = """
    INSERT INTO book_tags (tag_id, book_id)
    VALUES (?, ?)
    """

    params = [tag_id, book_id]

    g.db_execute(sql, params)

@db.modify_db
def deattach_tag(tag_id, book_id):
    """
    Deattaches a tag from a book.

    Args:
        tag_id (int): Id of the tag
        book_id (int): Id of the book
    """
    
    sql = """
    DELETE FROM book_tags
    WHERE tag_id = ? AND book_id = ?
    """

    params = [tag_id, book_id]

    g.db_execute(sql, params)

@db.modify_db
def remove_all_user_tags(user_id):
    """
    Removes all tags of a user (when user is removed)

    Args:
        user_id (int): Id of the user
    """
    
    sql_delete_from_tags = """
    DELETE FROM tags
    WHERE user_id = ?
    """

    sql_delete_from_book_tags = """
    DELETE FROM book_tags
    WHERE EXISTS (
        SELECT 1 FROM tags
        WHERE tags.user_id = ? AND tags.user_id = book_tags.tag_id
        )
    """

    params = [user_id]

    g.db_execute(sql_delete_from_book_tags, params)
    g.db_execute(sql_delete_from_tags, params)

@db.modify_db
def rename_tag(tag_id, new_name):
    """
    Renames an existing tag. Cannot have same name as user's other tags or global tags

    Args:
        tag_id (int): Id of the tag
        new_name (str): new name for the tag
    """
    
    sql = """
    UPDATE tags
    SET name = ?
    WHERE id = ?
    """

    params = [new_name, tag_id]

    g.db_execute(sql, params)

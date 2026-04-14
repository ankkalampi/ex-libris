import db
import user

@db.modify_db
def create_tag(user_id, name):
    """
    Creates a new tag onto db. Name cannot be same as user's other tags or global tags.

    Args:
        user_id (int): User id of the tag owner
        name (str): Tag name
    """
    pass

@db.modify_db
def create_global_tag(name):
    """
    Creates a global tag onto db. Global tags have NULL as user_id value. Cannot be same as other global tags.

    Args:
        name (str): Tag name
    """
    pass

@db.modify_db
def remove_tag(user_id, tag_id):
    """
    Deletes user tag from db and deattaches it from all user books.

    Args:
        user_id (int): Id of the user
        tag_id (int): Id of the tag
    """
    pass

@db.query_db
def get_user_tags(user_id):
    """
    Returns a list of all the tags (except global ones) of a user.

    Args:
        user_id (int): Id of the user

    Returns:
        List[Tuple(str)]: List of tag names as single value tuples
    """
    pass

@db.query_db
def get_global_tags():
    """
    Returns a list of all global tags.

    Returns:
        List[Tuple(str)]: List of tag names as single value tuples
    """
    pass

@db.modify_db
def attach_tag(tag_id, book_id):
    """
    Attaches a tag onto a book.

    Args:
        tag_id (int): Id of the tag
        book_id (int): Id of the book
    """
    pass

@db.modify_db
def deattach_tag(tag_id, book_id):
    """
    Deattaches a tag from a book.

    Args:
        tag_id (int): Id of the tag
        book_id (int): Id of the book
    """
    pass

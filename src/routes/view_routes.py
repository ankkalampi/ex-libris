"""
This module contains all routes that handle rendering views.
"""

import math
from flask import Blueprint, session, url_for, render_template, request, redirect
from src.services import shelf
from src.services import book
from src.services.user import login_required
from src.services import tag

view_bp = Blueprint('view', __name__)

@view_bp.get("/")
def index():
    """Route for front page view"""

    login_message = session.pop('login_message', None)
    return render_template("index_view/index.html", login_message=login_message)

@view_bp.get("/register")
def register():
    """Route for register view"""

    register_message = session.pop('register_message', None)
    return render_template("index_view/register.html", register_message=register_message)

@view_bp.get("/<username>")
@login_required
def profile(username):
    """Route for user profile view"""

    try:
        number_of_books = book.get_number_of_all_books(session["user_id"])
        number_of_shelves = shelf.get_number_of_all_shelves(session["user_id"])
    except Exception:
        return redirect(url_for("index"))

    return render_template("profile_view/profile.html",
                           username=username,
                           number_of_books=number_of_books,
                           number_of_shelves=number_of_shelves)

@view_bp.get("/<username>/hyllyt/<int:page>")
@login_required
def shelves(username, page=1):
    """Route for user bookshelves view"""

    user_id = session["user_id"]

    page_size = 10
    shelf_count = shelf.get_number_of_all_shelves(user_id)
    page_count = math.ceil(shelf_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/"+username+"/"+str(1))
    if page > page_count:
        return redirect("/"+username+"/"+str(page_count))


    try:
        shelves = shelf.get_shelves(user_id, page, page_size)
    except Exception:
        return redirect(url_for("index"))
    return render_template("shelves_view/shelves.html",
                           shelves=shelves, page=page,
                           page_count=page_count)

@view_bp.get("/<username>/uusi-hylly")
@login_required
def new_shelf_view(username):
    """
    Route for new shelf creation view

    Args:
        username (str): username of the current user
    """

    return render_template("shelves_view/new_shelf_view.html")

@view_bp.get("/<username>/hyllyt/<shelf_name>")
@login_required
def shelf_view(username, shelf_name):
    """
    Route for inside of a single shelf view

    Args:
        username (str): username of the current user
        shelf_name (str): name of the shelf
    """

    user_id = session["user_id"]
    add_book_message = session.pop('add_book_message', None)

    try:
        shelf_entry = shelf.get_shelf(shelf_name, user_id)
    except Exception:
        return redirect(url_for("index"))

    try:
        books = book.get_books(shelf_name, user_id)
    except Exception:
        username = session["username"]
        return redirect(url_for("shelf_view", shelf_name=shelf_name, username=username))

    return render_template("shelf_view/shelf_view.html",
                           shelf=shelf_entry,
                           books=books,
                           add_book_message=add_book_message)

@view_bp.get("/<username>/<shelf_name>/uusi-kirja")
@login_required
def new_book_view(username, shelf_name):
    """
    Route for creating a new book view

    Args:
        username (str): username of the current user
        shelf_name (str): name of the shelf
    """

    add_book_message = session.pop("add_book_message", None)
    tags = tag.get_all_tags()
    return render_template(
        "shelf_view/new_book_view.html",
        username=username,
        shelf_name=shelf_name,
        tags = tags,
        add_book_message=add_book_message)

@login_required
@view_bp.get("/<username>/<shelf_name>/muokkaa_kirjaa/<book_id>")
def modify_book_view(username, shelf_name, book_id):
    """
    Route for modifying a book view

    Args:
        username (str): username of the current user
        shelf_name (str): name of the shelf
        book_id (int): Id of the book
    """

    tags = tag.get_all_tags()
    try:
        book_entry = book.get_book(book_id)
    except Exception:
        session["book_modification_message"] = "kirjan tietojen hakemisessa tapahtui virhe"

    book_modification_message = session.pop("book_modification_message", None)
    return render_template("modify_book_view/modify_book_view.html",
                           tags = tags,
                           book=book_entry,
                           book_modification_message=book_modification_message,
                           shelf_name=shelf_name)

@view_bp.get("/<username>/haku")
@login_required
def search(username):
    """
    Route for searching books

    Args:
        username (str): username of the current user
    """
    tags = tag.get_all_tags()
    user_id = session["user_id"]
    name = request.args.get("name")
    author = request.args.get("author")
    year = request.args.get("year")
    isbn = request.args.get("isbn")
    if request.args.get("search-with-tag"):
        tag_id = request.args.get("tag_list")
    else:
        tag_id = None

    public = 1 if request.args.get("search-from-everyone-choice") else 0
    if name or author or year or isbn:
        try:
            result = book.search(name, author, year, isbn, public, user_id, tag_id)
        except Exception:
            return redirect(url_for("search"))
    else:
        result = []

    return render_template(
        "search_view/search_view.html",
        name=name,
        author=author,
        year=year,
        isbn=isbn,
        result=result,
        username=username,
        tag_id=tag_id,
        tags=tags)

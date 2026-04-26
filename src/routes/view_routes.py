from flask import Blueprint, session, url_for, render_template, request, redirect
import src.services.shelf as shelf
import src.services.book as book
from src.services.user import login_required
import src.services.tag as tag 
import math

view_bp = Blueprint('view', __name__)

@view_bp.get("/")
def index():
    """renders view for front page"""
    login_message = session.pop('login_message', None)
    return render_template("index_view/index.html", login_message=login_message)

@view_bp.get("/register")
def register():
    """renders view for register new user"""
    register_message = session.pop('register_message', None)
    return render_template("index_view/register.html", register_message=register_message)

@view_bp.get("/<username>")
@login_required
def profile(username):
    """renders view for user profile"""

    try:
        number_of_books = book.get_number_of_all_books(session["user_id"])
        number_of_shelves = shelf.get_number_of_all_shelves(session["user_id"])
    except Exception:
        return redirect(url_for("index"))

    return render_template("profile_view/profile.html", username=username, number_of_books=number_of_books, number_of_shelves=number_of_shelves)

@view_bp.get("/<username>/hyllyt/<int:page>")
@login_required
def shelves(username, page=1):
    """renders view for a user's bookshelves"""

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
    return render_template("shelves_view/shelves.html", shelves=shelves, page=page, page_count=page_count)

@view_bp.get("/<username>/uusi-hylly")
@login_required
def new_shelf_view(username):
    """renders view for creation of new shelf"""

    return render_template("shelves_view/new_shelf_view.html")

@view_bp.get("/<username>/hyllyt/<shelf_name>")
@login_required
def shelf_view(username, shelf_name):
    """renders view for a single shelf"""

    user_id = session["user_id"]

    try:
        shelf_entry = shelf.get_shelf(shelf_name, user_id)
    except Exception:
        return redirect(url_for("index"))

    try:
        books = book.get_books(shelf_name, user_id)
    except Exception:
        username = session["username"]
        return redirect(url_for("shelf_view", shelf_name=shelf_name, username=username))

    return render_template("shelf_view/shelf_view.html", shelf=shelf_entry, books=books)

@view_bp.get("/<username>/<shelf_name>/uusi-kirja")
@login_required
def new_book_view(username, shelf_name):
    """renders view for adding a book to a shelf"""
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
    tags = tag.get_all_tags()
    try:
        book_entry = book.get_book(book_id)
    except Exception:
        session["book_modification_message"] = "kirjan tietojen hakemisessa tapahtui virhe"

    book_modification_message = session.pop("book_modification_message", None)
    return render_template("modify_book_view/modify_book_view.html", tags = tags, book=book_entry, book_modification_message=book_modification_message, shelf_name=shelf_name)

@view_bp.get("/<username>/haku/<int:page>")
@login_required
def search(username, page=1):
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

import sys
import math
import secrets
from pathlib import Path
from flask import Flask
from flask import session, g, url_for, redirect, request, render_template
import config
import user
import book
import shelf
import tag


sys.path.append(str(Path(__file__).parent / "src"))


app = Flask(__name__)
app.secret_key = config.secret_key

@app.before_request
def load_logged_in_user():
    """
    Sets the user variable for g object before a request is made
    """
    username = session.get("username")
    if username is None:
        g.user = None
    else:
        g.user = username

@app.post("/create_book/<username>/<shelf_name>")
@user.login_required
@user.csrf_required
def create_book(username, shelf_name):
    """
    Route for creating a new book

        Args:
            username (str): current user username
            shelf_name (str): shelf name
    """

    name = request.form["name"]
    author = request.form["author"]
    pages = request.form["pages"]
    synopsis = request.form["synopsis"]
    isbn = request.form["isbn"]
    year = request.form["year"]
    tag_id = request.form["tag_list"]
    user_id = session["user_id"]

    if pages == "":
        pages = 0

    if isbn == "":
        isbn = None

    if year == "":
        year = 'tuntematon'

    if name == "" or author == "":
        session["add_book_message"] = "Kirjan nimi sekä kirjoittajan nimi vaaditaan!"
        return redirect(
            url_for(
                "view.new_book_view",
                username=username,
                shelf_name=shelf_name))

    try:
        book.create_book(
            user_id,
            shelf_name,
            name,
            author,
            pages,
            year,
            isbn,
            synopsis,
            tag_id)

    except Exception as e:
        print(e)
        session["add_book_message"] = "VIRHE: Kirja on jo olemassa"
        return redirect(
            url_for(
                "view.new_book_view",
                username=username,
                shelf_name=shelf_name))

    session["add_book_message"] = "Kirja lisätty!"
    return redirect(
        url_for(
            "view.shelf_view",
            username=username,
            shelf_name=shelf_name))

@user.login_required
@user.csrf_required
@app.post("/modify_book/<username>/<shelf_name>/<book_id>")
def modify_book(book_id, username, shelf_name):
    """
    Route for modifying book

    Args:
        book_id (int): Id of the book
        username (str): username of the current user (for redirecting)
        shelf_name (str): name of the shelf
    """

    name = request.form["name"]
    author = request.form["author"]
    ISBN = request.form["isbn"]
    year = request.form["year"]
    synopsis = request.form["synopsis"]
    pages = request.form["pages"]
    tag_id  = request.form["tag_list"]

    if name == "":
        name = None
    if author == "":
        author = None
    if year == "":
        year = None
    if ISBN == "":
        ISBN = None
    if synopsis == "":
        synopsis = None
    if pages == "":
        pages = None

    try:
        book.modify_book(
            book_id,
            name,
            author,
            year,
            synopsis,
            ISBN,
            pages,
            tag_id)
    except book.BookModificationFieldsEmpty as e:
        session["book_modification_message"] = str(e)
        return redirect(url_for("view.modify_book_view",
                                username=username,
                                book_id=book_id,
                                shelf_name=shelf_name))
    except Exception as e:
        print(e)
        session["book_modification_message"] = "kirja näillä tiedoilla on jo olemassa"
        return redirect(
            url_for(
                "view.modify_book_view",
                username=username,
                book_id=book_id,
                shelf_name=shelf_name
            )
        )

    session["book_modification_message"] = "Kirja muokattu onnistuneesti!"

    return redirect(
        url_for(
            "view.modify_book_view",
            username=username,
            shelf_name=shelf_name,
            book_id=book_id
        ))

@user.login_required
@user.csrf_required
@app.post("/remove_book/<username>/<shelf_name>/<book_id>")
def remove_book(book_id, username, shelf_name):
    """
    Route for removing a book

    Args:
        book_id (int): Id of the book
        username (str): username of the current user
        shelf_name (str): name of the shelf
    """
    try:
        book.remove_book(book_id)

    except Exception:
        session["book_delete_message"] = "VIRHE Kirjaa ei onnistuttu poistamaan"
        return redirect(
            url_for(
                "view.shelf_view",
                username=username,
                shelf_name=shelf_name
            )
        )

    return redirect(url_for("view.shelf_view", username=username, shelf_name=shelf_name))

def get_page_count(page_size):
    """"
    Get page count for paging

    Args:
        page_size (int): desired page size

    Returns:
        (int)
    """

    user_id = session["user_id"]
    shelf_count = shelf.get_number_of_all_shelves(user_id)
    page_count = math.ceil(shelf_count / page_size)
    page_count = max(page_count, 1)

    return page_count

@app.post("/create_shelf")
@user.login_required
@user.csrf_required
def create_shelf():
    """Route for creating a new bookshelf"""
    username = session["username"]
    user_id = session["user_id"]

    name = request.form["name"]
    description = request.form["description"]
    public = 1 if request.form.get("public-choice") else 0

    page_count = get_page_count(10)

    try:
        shelf.create_shelf(user_id, name, description, public)
    except Exception:
        return redirect(url_for("view.index"))

    return redirect(url_for("view.shelves",
                            username=username,
                            page_count=page_count,
                            page=1))

@app.get("/remove_shelf/<username>/<shelf_id>")
@user.login_required
def remove_shelf(username, shelf_id):
    """
    Route for removing a bookshelf

    Args:
        username (str): username of the current user
        shelf_id (int): Id of the shelf
    """

    page_count = get_page_count(10)

    try:
        shelf.delete_shelf(shelf_id)
    except Exception:
        return redirect(url_for("view.index"))

    return redirect(url_for("view.shelves",
                            username=username,
                            page_count=page_count,
                            page=1))

@app.post("/create")
def create():
    """Route for creating a new user"""

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        session["register_message"] = "VIRHE! salasanat eivät ole samat"
        return redirect(url_for("view.register"))

    try:
        user.create_user(username, password1)
    except Exception:
        return redirect(url_for("view.register"))

    session["login_message"] = "Käyttäjä luotu!"
    return redirect(url_for("view.index"))

@app.post("/login")
def login():
    """Route for logging in user"""

    username = request.form["username"]
    password = request.form["password"]

    session["csrf_token"] = secrets.token_hex(16)

    if user.login(username, password):
        return redirect(url_for("view.profile", username=username))

    return redirect(url_for("view.index"))

@app.get("/logout")
@user.login_required
def logout():
    """Route for logging out user"""

    del session["username"]
    return redirect(url_for("view.index"))

@app.get("/")
def index():
    """Route for front page view"""

    login_message = session.pop('login_message', None)
    return render_template("index_view/index.html", login_message=login_message)

@app.get("/register")
def register():
    """Route for register view"""

    register_message = session.pop('register_message', None)
    return render_template("index_view/register.html", register_message=register_message)

@app.get("/<username>")
@user.login_required
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

@app.get("/<username>/hyllyt/<int:page>")
@user.login_required
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
        user_shelves = shelf.get_shelves(user_id, page, page_size)
    except Exception:
        return redirect(url_for("index"))
    return render_template("shelves_view/shelves.html",
                           shelves=user_shelves, page=page,
                           page_count=page_count)

@app.get("/<username>/uusi-hylly")
@user.login_required
def new_shelf_view(username):
    """
    Route for new shelf creation view

    Args:
        username (str): username of the current user
    """

    return render_template("shelves_view/new_shelf_view.html")

@app.get("/<username>/hyllyt/<shelf_name>")
@user.login_required
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

@app.get("/<username>/<shelf_name>/uusi-kirja")
@user.login_required
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

@user.login_required
@app.get("/<username>/<shelf_name>/muokkaa_kirjaa/<book_id>")
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

@app.get("/<username>/haku")
@user.login_required
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
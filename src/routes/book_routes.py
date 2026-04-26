from flask import Blueprint, session, url_for, redirect, request
import src.services.book as book
from src.services.user import login_required, csrf_required

book_bp = Blueprint('book', __name__)


@book_bp.post("/create_book/<username>/<shelf_name>")
@login_required
@csrf_required
def create_book(username, shelf_name):
    """Route for creating a new book"""

    name = request.form["name"]
    author = request.form["author"]
    pages = request.form["pages"]
    synopsis = request.form["synopsis"]
    isbn = request.form["isbn"]
    year = request.form["year"]
    tag_id = request.form["tag_list"]
    user_id = session["user_id"]

    if (pages == ""):
        pages = 0

    if (isbn == ""):
        isbn = None

    if (year == ""):
        year = 'tuntematon'

    if (name == "" or author == ""):
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
            "view.new_book_view",
            username=username,
            shelf_name=shelf_name))


@login_required
@csrf_required
@book_bp.post("/modify_book/<username>/<shelf_name>/<book_id>")
def modify_book(book_id, username, shelf_name):

    name = request.form["name"]
    author = request.form["author"]
    ISBN = request.form["isbn"]
    year = request.form["year"]
    synopsis = request.form["synopsis"]
    pages = request.form["pages"]
    tag_id  = request.form["tag_list"]
    user_id = session["user_id"]

    print("REQUEST:")
    print(f"name: {name}")
    print(f"author: {author}")
    print(f"ISBN: {ISBN}")
    print(f"year: {year}")
    print(f"synopsis: {synopsis}")
    print(f"pages: {pages}")
    print(f"tag_id: {tag_id}")
    print(f"user_id: {user_id}")


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
        return redirect(url_for("view.modify_book_view", username=username, book_id=book_id, shelf_name=shelf_name))
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

    print("no exceptions, redirecting to modify_book_view")

    session["book_modification_message"] = "Kirja muokattu onnistuneesti!"

    return redirect(
        url_for(
            "view.modify_book_view",
            username=username,
            shelf_name=shelf_name,
            book_id=book_id
        ))


@login_required
@csrf_required
@book_bp.post("/remove_book/<username>/<shelf_name>/<book_id>")
def remove_book(book_id, username, shelf_name):
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

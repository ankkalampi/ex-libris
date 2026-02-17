from flask import Flask
from flask import render_template, redirect, request
from flask import session, url_for, g
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import db
import shelf
import user
import book
import config
from user import login_required
from markupsafe import escape

app = Flask(__name__)
app.secret_key = config.secret_key

@app.before_request
def load_logged_in_user():
    username = session.get("username")
    if username is None:
        g.user = None
    else:
        g.user = username


@app.get("/")
def index():
	"""renders view for front page"""
	login_message = session.pop('login_message', None)
	return render_template("index.html", login_message=login_message)

@app.get("/register")
def register():
	"""renders view for register new user"""
	register_message = session.pop('register_message', None)
	return render_template("register.html", register_message=register_message)

@app.post("/create")
def create():
	"""creates new user"""
	username = request.form["username"]
	password1 = request.form["password1"]
	password2 = request.form["password2"]

	if password1 != password2:
		session["register_message"] = "VIRHE! salasanat eivät ole samat"
		return redirect(url_for("register"))
	
	user.create_user(username, password1, password2)

	session["login_message"] = "Käyttäjä luotu!"
	return redirect(url_for("index"))

@app.post("/login")
def login():
	"""attempts to log in user"""
	username = request.form["username"]
	password = request.form["password"]

	if user.login(username, password):
		return redirect(url_for("profile", username=username))
	else:
		return redirect(url_for("index"))


@app.get("/logout")
@login_required
def logout():
	"""logs in user"""
	del session["username"]
	return redirect(url_for("index"))

@app.get("/<username>")
@login_required
def profile(username):
	"""renders view for user profile"""

	return render_template("profile.html", username=username)

@app.get("/<username>/hyllyt")
@login_required
def shelves(username):
	"""renders view for a user's bookshelves"""

	

	shelves = shelf.get_shelves(username)


	return render_template("shelves.html", shelves=shelves)

@app.post("/create_shelf")
@login_required
def create_shelf():
	"""creates new bookshelf"""
	username = session["username"]


	name = request.form["name"]
	description = request.form["description"]
	public = 1 if request.form.get("public-choice") else 0

	shelf.create_shelf(username, name, description, public)

	return redirect(url_for("shelves", username=username))

@app.get("/<username>/uusi-hylly")
@login_required
def new_shelf_view(username):
	"""renders view for creation of new shelf"""

	return render_template("new_shelf_view.html")

@app.get("/remove_shelf/<username>/<shelf_id>")
@login_required
def remove_shelf(username, shelf_id):
	"""removes bookshelf"""
	shelf.delete_shelf(shelf_id)
	return redirect(url_for("shelves", username=username))

@app.get("/<username>/hyllyt/<shelf_name>")
@login_required
def shelf_view(username, shelf_name):
	"""renders view for a single shelf"""

	shelf_entry = shelf.get_shelf(shelf_name, username)


	books = book.get_books(shelf_name, username)

	return render_template("shelf_view.html", shelf=shelf_entry, books=books)

@app.get("/<username>/<shelf_name>/uusi-kirja")
@login_required
def new_book_view(username, shelf_name):
	"""renders view for adding a book to a shelf"""
	add_book_message = session.pop("add_book_message", None)
	return render_template("new_book_view.html", username=username, shelf_name=shelf_name, add_book_message=add_book_message)

@app.post("/create_book/<username>/<shelf_name>")
@login_required
def create_book(username, shelf_name):
	"""creates a new book"""

	name = request.form["name"]
	author = request.form["author"]
	pages = request.form["pages"]
	synopsis = request.form["synopsis"]

	if (synopsis == ""):
		synopsis = None

	if (pages == 0):
		pages = None

	if (name == "" or author == ""):
		session["add_book_message"] = "Kirjan nimi sekä kirjoittajan nimi vaaditaan!"
		return redirect(url_for("new_book_view", username=username, shelf_name=shelf_name))
		

	try:
		book.create_book(username, shelf_name, name, author, pages, synopsis)
	except:
		session["add_book_message"] = "VIRHE: Kirja on jo olemassa"
		return redirect(url_for("new_book_view", username=username, shelf_name=shelf_name))

	session["add_book_message"] = "Kirja lisätty!"
	return redirect(url_for("new_book_view", username=username, shelf_name=shelf_name))





@app.get("/<username>/haku")
def search(username):
	name = request.args.get("name")
	author = request.args.get("author")
	public = 1 if request.args.get("search-from-everyone-choice") else 0
	result = book.search(name, author, public, username) if name else []
	return render_template("search_view.html", name=name, author=author, result=result, username=username)
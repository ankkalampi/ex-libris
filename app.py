from flask import Flask
from flask import render_template, redirect, request
from flask import session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import db
import shelf
import user
app = Flask(__name__)
app.secret_key = 'secret key'

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
		return redirect("/register")
	
	user.create_user(username, password1, password2)

	session["login_message"] = "Käyttäjä luotu!"
	return redirect("/")

@app.post("/login")
def login():
	"""attempts to log in user"""
	username = request.form["username"]
	password = request.form["password"]

	if user.login(username, password):
		return redirect(url_for("profile", username=username))
	else:
		return redirect("/")


@app.get("/logout")
def logout():
	"""logs in user"""
	del session["username"]
	return redirect("/")

@app.get("/<username>")
def profile(username):
	"""renders view for user profile"""

	return render_template("profile.html", username=username)

@app.get("/<username>/hyllyt")
def shelves(username):
	"""renders view for a user's bookshelves"""

	

	shelves = shelf.get_shelves(username)


	return render_template("shelves.html", shelves=shelves)

@app.post("/create_shelf")
def create_shelf():
	"""creates new bookshelf"""
	username = session["username"]


	name = request.form["name"]
	description = request.form["description"]

	shelf.create_self(username, name, description)

	return redirect(f"/{username}/hyllyt")

@app.get("/<username>/uusi-hylly")
def new_shelf_view(username):
	"""renders view for creation of new shelf"""

	return render_template("new_shelf_view.html")

@app.get("/remove_shelf/<username>/<shelf_id>")
def remove_shelf(username, shelf_id):
	shelf.delete_shelf(shelf_id)
	return redirect(f"/{username}/hyllyt")



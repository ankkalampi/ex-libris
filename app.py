from flask import Flask
from flask import render_template, redirect, request
from flask import session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import db
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

	password_hash = generate_password_hash(password1)

	try:
		sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
		db.execute(sql, [username, password_hash])
	except sqlite3.IntegrityError:
		session["register_message"] = "VIRHE: tunnus on jo varattu"
		return redirect("/register")

	session["login_message"] = "Käyttäjä luotu!"
	return redirect("/")

@app.post("/login")
def login():
	"""attempts to log in user"""
	username = request.form["username"]
	password = request.form["password"]

	sql = "SELECT password_hash FROM users WHERE username = ?"
	result = db.query(sql, [username])

	if not result:
		session["login_message"] = "Käyttäjää ei löydy"
		return redirect("/")

	password_hash = result[0][0]

	if check_password_hash(password_hash, password):
		session["username"] = username
		return redirect(url_for("profile", username=username))
	else:
		session["login_message"] = "Väärä käyttäjätunnus tai salasana"
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

	

	try:
		sql = "SELECT id FROM users WHERE username = ?"
		result = db.query(sql, [username])
		user_id = result[0][0]
	except:
		print(f"Database error in finding user id user_id: {user_id}")
		return redirect("/")

	try:
		sql = "SELECT name, number_of_books, description FROM shelves WHERE user_id = ?"
		shelves = db.query(sql, [user_id])
	except:
		print(f"Database error in selecting shelves, user_id: {user_id}")
		return redirect("/")


	return render_template("shelves.html", shelves=shelves)

@app.post("/create_shelf")
def create_shelf():
	"""creates new bookshelf"""
	username = session["username"]

	try:
		sql = "SELECT id FROM users WHERE username = ?"
		result = db.query(sql, [username])
		user_id = result[0][0]
	except:
		print(f"Database error in finding user id, user_id: {user_id} ")
		return redirect("/")

	name = request.form["name"]
	description = request.form["description"]

	try:
		sql = "INSERT INTO shelves (user_id, name, number_of_books, description) VALUES (?, ?, ?, ?)"
		db.execute(sql, [user_id, name, 0, description])
	except:
		print("Database error in creating new shelf")
		return redirect ("/")

	return redirect(f"/{username}/hyllyt")

@app.get("/<username>/uusi-hylly")
def new_shelf_view(username):
	"""renders view for creation of new shelf"""

	return render_template("new_shelf_view.html")



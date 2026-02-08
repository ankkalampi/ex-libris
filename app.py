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
	

	login_message = session.pop('login_message', None)
	return render_template("index.html", login_message=login_message)

@app.get("/register")
def register():
	register_message = session.pop('register_message', None)
	return render_template("register.html", register_message=register_message)

@app.post("/create")
def create():
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

	username = request.form["username"]
	password = request.form["password"]

	sql = "SELECT password_hash FROM users WHERE username = ?"
	result = db.query(sql, [username])

	print("the result is: ", result)
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
	del session["username"]
	return redirect("/")

@app.get("/<username>")
def profile(username):

	return render_template("profile.html", username=username)
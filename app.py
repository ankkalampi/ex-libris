from flask import Flask
from flask import render_template
import sqlite3
import db
app = Flask(__name__)

@app.route("/")
def index():
	connection = db.get_connection()
	db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))", connection)
	result = db.query("SELECT COUNT(*) FROM visits", connection)
	count = result[0][0]
	connection.close()

	return render_template("index.html", count=count)

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
	username = request.form["username"]
	password1 = request.form["password1"]
	password2 = request.form["password2"]
	if password1 != password2:
		return "VIRHE: salasanat eivät ole samat"
	password_hash = generate_password_hash(password1)

	try:
		sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
		db.execute(sql, [username, password_hash])
	except sqlite3.IntegrityError:
		return "VIRHE: tunnus on jo varattu"

	return "Tunnus luotu"
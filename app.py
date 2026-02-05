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

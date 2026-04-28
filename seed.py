"""
Thos module creates test data for the application.
Remember to reset database using init_db.py before using this.
"""

import random
import sqlite3
from werkzeug.security import generate_password_hash

dbx = sqlite3.connect("database.db")
db = dbx.cursor()
db.execute("PRAGMA foreign_keys = ON;")

db.execute("DELETE FROM users")
db.execute("DELETE FROM books")
db.execute("DELETE FROM shelves")
db.execute("DROP INDEX idx_books_user_id")
db.execute("DROP INDEX idx_books_shelf_id")
db.execute("DROP INDEX idx_books_tag_id")
db.execute("DROP INDEX idx_books_name")
db.execute("DROP INDEX idx_books_author")
db.execute("DROP INDEX idx_books_year")
db.execute("DROP INDEX idx_books_ISBN")
db.execute("DROP INDEX idx_user_shelf_books")
db.execute("DROP INDEX idx_shelves_user_id")
db.execute("DROP INDEX idx_shelves_public")
dbx.commit()

USER_COUNT = 200
SHELF_COUNT_PER_USER = 20
BOOK_COUNT_BY_SHELF = 500

password_hash = generate_password_hash("password")

shelf_id = 0
book_id = 0
for user_i in range(1, USER_COUNT + 1):
    try:
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                   ["user" + str(user_i), password_hash])
        dbx.commit()
        user_id = db.lastrowid
        print(f"user id: {user_id}/{USER_COUNT} ")
    except Exception as e:
        print("something happened")
        print(e)
    for shelf_i in range(1, SHELF_COUNT_PER_USER + 1):
        db.execute("INSERT INTO shelves (user_id, name, description, public) VALUES (?, ?, ?, ?)",
                [user_id, "shelf" + str(shelf_id), "", 1])
        dbx.commit()
        shelf_id = db.lastrowid

        for book_i in range(1, BOOK_COUNT_BY_SHELF + 1):
            db.execute("""INSERT INTO books (name, author, year, user_id, shelf_id, tag_id)
                        VALUES (?,?,?,?, ?,?)""",
                    ["book"+str(book_id),
                     "author"+str(book_id),
                     random.randint(1, 5000),
                     user_id, shelf_id, 5])

            book_id += 1
dbx.commit()

db.execute("CREATE INDEX idx_books_user_id ON books(user_id);")
db.execute("CREATE INDEX idx_books_shelf_id ON books(shelf_id);")
db.execute("CREATE INDEX idx_books_tag_id ON books(tag_id);")
db.execute("CREATE INDEX idx_books_name ON books(name);")
db.execute("CREATE INDEX idx_books_author ON books(author);")
db.execute("CREATE INDEX idx_books_year ON books(year);")
db.execute("CREATE INDEX idx_books_ISBN ON books(ISBN);")
db.execute("CREATE INDEX idx_user_shelf_books ON books(shelf_id, user_id);")

db.execute("CREATE INDEX idx_shelves_user_id ON shelves(user_id);")
db.execute("CREATE INDEX idx_shelves_public ON shelves(id) WHERE public = 1;")

dbx.commit()

dbx.close()

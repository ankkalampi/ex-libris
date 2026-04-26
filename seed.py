import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM books")
db.execute("DELETE FROM shelves")

user_count = 1000
shelf_count = 10**5
book_count = 10**7

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               ["user" + str(i), "passwd"])

for i in range(1, shelf_count + 1):
    db.execute("INSERT INTO shelves (user_id, name, description, public) VALUES (?, ?, ?, ?)",
               [random.randint(1, user_count), "shelf" + str(i), "", 1])

for i in range(1, book_count + 1):
    user_id = 1
    shelf_id = random.randint(1, shelf_count)
    db.execute("""INSERT INTO books (name, author, year, user_id, shelf_id, tag_id)
                  VALUES (?,?,?,?, ?,?)""",
               ["book"+str(i), "author"+str(i), random.randint(1, 5000), user_id, shelf_id, 5])

    
    db.execute("INSERT INTO shelf_books (shelf_id, book_id) VALUES ((SELECT id FROM shelves WHERE id = ?), ?)",
               [shelf_id, i])
db.commit()
db.close()

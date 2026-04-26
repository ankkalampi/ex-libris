DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS shelves;
DROP TABLE IF EXISTS user_books;
DROP TABLE IF EXISTS shelf_books;

CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	username TEXT UNIQUE NOT NULL,
	password_hash TEXT NOT NULL
);

CREATE TABLE books (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	author TEXT NOT NULL,
	year TEXT NOT NULL,
	ISBN TEXT UNIQUE,
	pages INTEGER,
	synopsis TEXT,
	user_id INTEGER,
	shelf_id INTEGER NOT NULL,
	tag_id INTEGER NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE, 
	FOREIGN KEY (tag_id) REFERENCES tags(id),
	FOREIGN KEY (shelf_id) REFERENCES shelves(id) ON DELETE CASCADE ON UPDATE CASCADE,
	UNIQUE (name, author, year, user_id, shelf_id)
);

CREATE TABLE tags (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL
);

CREATE TABLE shelves (
	id INTEGER PRIMARY KEY,
	user_id INTEGER NOT NULL,
	name TEXT NOT NULL,
	description TEXT NOT NULL,
	public INTEGER NOT NULL CHECK (public IN (0,1)),
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE user_books (
	user_id INTEGER NOT NULL,
	book_id INTEGER NOT NULL,
	PRIMARY KEY (user_id, book_id),
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE shelf_books (
	shelf_id INTEGER NOT NULL,
	book_id INTEGER NOT NULL,
	PRIMARY KEY (shelf_id, book_id),
	FOREIGN KEY (shelf_id) REFERENCES shelves(id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (book_id) REFERENCES books(id)
);

CREATE INDEX idx_books_user_id ON books(user_id);
CREATE INDEX idx_books_shelf_id ON books(shelf_id);
CREATE INDEX idx_books_tag_id ON books(tag_id);
CREATE INDEX idx_shelves_user_id ON shelves(user_id);

CREATE INDEX idx_user_books_book_id ON user_books(user_id);
CREATE INDEX idx_shelf_books_shelf_id ON shelf_books(shelf_id);
CREATE INDEX idx_shelves_public ON shelves(id) WHERE public = 1;

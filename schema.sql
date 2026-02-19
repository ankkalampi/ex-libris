CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	username TEXT UNIQUE NOT NULL,
	password_hash TEXT NOT NULL
);

CREATE TABLE books (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	author TEXT NOT NULL,
	pages INTEGER,
	synopsis TEXT,
	user_id INTEGER,
	UNIQUE (name, author, user_id)

);

CREATE TABLE tags (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL
);

CREATE TABLE shelves (
	id INTEGER PRIMARY KEY,
	user_id INTEGER NOT NULL,
	name TEXT NOT NULL,
	description TEXTNOT NULL,
	public INTEGER NOT NULL CHECK (public IN (0,1)),
	FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE book_tags (
	book_id INTEGER NOT NULL,
	tag_id INTEGER NOT NULL,
	PRIMARY KEY (book_id, tag_id),
	FOREIGN KEY (book_id) REFERENCES books(id),
	FOREIGN KEY (tag_id) REFERENCES tags(id)
);

CREATE TABLE user_books (
	user_id INTEGER NOT NULL,
	book_id INTEGER NOT NULL,
	PRIMARY KEY (user_id, book_id),
	FOREIGN KEY (user_id) REFERENCES users(id),
	FOREIGN KEY (book_id) REFERENCES books(id)
);


CREATE TABLE shelf_books (
	shelf_id INTEGER NOT NULL,
	book_id INTEGER NOT NULL,
	PRIMARY KEY (shelf_id, book_id),
	FOREIGN KEY (shelf_id) REFERENCES shelves(id),
	FOREIGN KEY (book_id) REFERENCES books(id)
);

CREATE INDEX idx_user_books_book_id ON user_books(user_id);
CREATE INDEX idx_shelf_books_book_id ON shelf_books(book_id);
CREATE INDEX idx_shelf_id ON shelves(id);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_shelves_public ON shelves(id) WHERE public = 1;
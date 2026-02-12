CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	username TEXT UNIQUE,
	password_hash TEXT
);

CREATE TABLE books (
	id INTEGER PRIMARY KEY,
	name TEXT,
	author TEXT,
	pages INTEGER,
	synopsis TEXT,
	user_id INTEGER,
	UNIQUE (name, author, user_id)

);

CREATE TABLE tags (
	id INTEGER PRIMARY KEY,
	name TEXT
);

CREATE TABLE shelves (
	id INTEGER PRIMARY KEY,
	user_id INTEGER,
	name TEXT,
	number_of_books INTEGER,
	description TEXT,
	FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE book_tags (
	book_id INTEGER,
	tag_id INTEGER,
	PRIMARY KEY (book_id, tag_id),
	FOREIGN KEY (book_id) REFERENCES books(id),
	FOREIGN KEY (tag_id) REFERENCES tags(id)
);

CREATE TABLE user_books (
	user_id INTEGER,
	book_id INTEGER,
	PRIMARY KEY (user_id, book_id),
	FOREIGN KEY (user_id) REFERENCES users(id),
	FOREIGN KEY (book_id) REFERENCES books(id)
);


CREATE TABLE shelf_books (
	shelf_id INTEGER,
	book_id INTEGER,
	PRIMARY KEY (shelf_id, book_id),
	FOREIGN KEY (shelf_id) REFERENCES shelves(id),
	FOREIGN KEY (book_id) REFERENCES books(id)
);
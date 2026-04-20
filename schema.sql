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
	UNIQUE (name, author, year, user_id)
);

CREATE TABLE tags (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	user_id INTEGER,
	FOREIGN KEY (user_id) REFERENCES users(id),
	UNIQUE (user_id, name)
);

CREATE TABLE shelves (
	id INTEGER PRIMARY KEY,
	user_id INTEGER NOT NULL,
	name TEXT NOT NULL,
	description TEXT NOT NULL,
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
CREATE INDEX idx_shelf_books_shelf_id ON shelf_books(shelf_id);
CREATE INDEX idx_shelves_public ON shelves(id) WHERE public = 1;
CREATE INDEX idx_user_tags_user_id ON tags(user_id);
CREATE INDEX idx_book_tags_book_id ON book_tags(book_id);

CREATE TRIGGER check_for_global_tag_before_adding_new_tags
BEFORE INSERT ON tags
FOR EACH ROW
WHEN ( EXISTS (
	SELECT 1 FROM tags
	WHERE name = NEW.name AND user_id = NULL
))
BEGIN 
	SELECT RAISE (ABORT, 'Tag already exists as global tag');
END;

CREATE TRIGGER check_for_global_tag_before_modifying_new_tags
BEFORE UPDATE ON tags
FOR EACH ROW
WHEN ( EXISTS (
	SELECT 1 FROM tags
	WHERE name = NEW.name AND user_id = NULL
))
BEGIN 
	SELECT RAISE (ABORT, 'Tag already exists as global tag');
END;
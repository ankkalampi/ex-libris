CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	username TEXT UNIQUE,
	password_hash TEXT
);

CREATE TABLE visits (
	id INTEGER PRIMARY KEY,
	visited_at TEXT
);

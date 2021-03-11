CREATE TABLE users(
		userID INTEGER PRIMARY KEY AUTOINCREMENT,
		username VARCHAR(16),
		firstname VARCHAR(16),
		lastname VARCHAR(16),
		password VARCHAR(32)
	);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE lists(
		listID INTEGER PRIMARY KEY AUTOINCREMENT,
		userID INTEGER,
		listname VARCHAR(16),
		numberoftasks INTEGER
	);
CREATE TABLE tasks(
		taskID INTEGER PRIMARY KEY AUTOINCREMENT,
		listID INTEGER,
		taskname VARCHAR(16)
	);
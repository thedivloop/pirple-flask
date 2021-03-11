import sqlite3

connection = sqlite3.connect('project.db', check_same_thread = False)
cursor = connection.cursor()

cursor.execute(
	"""CREATE TABLE users(
		userID INTEGER PRIMARY KEY AUTOINCREMENT,
		username VARCHAR(16),
		firstname VARCHAR(16),
		lastname VARCHAR(16),
		password VARCHAR(32)
	); """
)

cursor.execute(
	"""CREATE TABLE lists(
		listID INTEGER PRIMARY KEY AUTOINCREMENT,
		userID INTEGER,
		listname VARCHAR(16),
		numberoftasks INTEGER
	); """
)

cursor.execute(
	"""CREATE TABLE tasks(
		taskID INTEGER PRIMARY KEY AUTOINCREMENT,
		listID INTEGER,
		taskname VARCHAR(16)
	); """
)



connection.commit()
cursor.close()
connection.close()
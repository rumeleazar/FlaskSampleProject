import sqlite3


#Open database
conn = sqlite3.connect('database.db')

#Create table

conn.execute('''DROP TABLE IF EXISTS user''') 
conn.execute('''DROP TABLE IF EXISTS recipe''') 
conn.execute('''DROP TABLE IF EXISTS readinglist''') 
conn.execute('''DROP TABLE IF EXISTS comments''') 

conn.execute('''CREATE TABLE user(id INTEGER  PRIMARY KEY, username VARCHAR(100) NOT NULL, password VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL, firstname VARCHAR(100) NOT NULL, lastname VARCHAR(100) NOT NULL )''')

conn.execute('''CREATE TABLE recipe(id INTEGER  PRIMARY KEY, dishname VARCHAR(100) NOT NULL, description TEXT NOT NULL, ingredients TEXT NOT NULL, directions TEXT NOT NULL, imagename VARCHAR(100) NOT NULL, author VARCHAR(100) NOT NULL, datetoday VARCHAR(100) NOT NULL) ''')

conn.execute('''CREATE TABLE readinglist(id INTEGER PRIMARY KEY, dishname VARCHAR(100) NOT NULL, author VARCHAR(100) NOT NULL, user VARCHAR(100) NOT NULL)''')

conn.execute('''CREATE TABLE  comments(comments TEXT NOT NULL, id INTEGER NOT NULL, user VARCHAR(100) NOT NULL, datetoday VARCHAR(100) NOT NULL)''')


#Close database cursor
conn.close()
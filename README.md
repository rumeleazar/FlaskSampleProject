# RecipeShareProject #
A simple recipe sharing CRUD website using Flask where you can create an account, log in, create a recipe and share it. 
  
## Dependencies ##
1. Python3
2. Flask
3. Sqlite3 ( If you have mySQL you can use it too. There are comments inside on how you can initialize the app to MySQL. Just remove all the " with sqlite3.connect('database.db') as conn: " and the " import sqlite3 ". Also, change all the "conn.cursor()" to "mysql.connection.cursor()" and the variables inside the executes from " ? " to " %s " )

## How to run ##
1. install all the requirements in the requirements.txt
2. install sqlite3 using pip install pysqlite3 (On windows. I still don't know how to do it on MAC and Linux, Maybe apt-get install sqlite3? ) 
3. Set up database by running database.py
4. Run application.py
5. Enter localhost:5000 in the browser.

### NOTE ### 
This project is still not finished. There are still some work to do:
1. The search bar is still not working
2. Create a functionality where the users can like/heart or rate the recipe
3. Make the ingredients and directions to be a list instead of just plain text
4. Make the website responsive
5. The website design
6. Add the date when the recipe is created


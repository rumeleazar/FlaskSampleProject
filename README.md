# RecipeShareProject #
A simple recipe sharing CRUD website using Flask where you can create an account, log in, create a recipe and share it. Visit the project at: http://recipeshare.glitch.me/

Note: The project is hosted at glitch.com. glitch.com has a function that makes the project/website sleep when nobody is visiting it, so it resets everything and deletes the data in the database(accounts, recipes, comments, etc.) when it sleeps.
  
## Dependencies ##
1. Python3
2. Flask
3. Sqlite3 ( If you have mySQL you can use it too. There are comments inside on how you can initialize the app to MySQL. Just remove all the " with sqlite3.connect('database.db') as conn: " and the " import sqlite3 ". Also, change all the "conn.cursor()" to "mysql.connection.cursor()" and the variables inside the executes from " ? " to " %s " )

## How to run ##
1. install all the requirements in the requirements.txt
2. install sqlite3 using pip install pysqlite3 (On windows. I still don't know how to do it on MAC and Linux, Maybe apt-get install sqlite3? ) 
3. Change the path of the static folder in the application.py and adjust it to your machines path
4. Set up database by running database.py
5. Run application.py
6. Enter localhost:5000 in the browser.

## NOTES ##
This project is still not finished. There are still some work to do:
1. The search bar is still not working (Done)
2. Create a functionality where the users can like/heart or rate the recipe
3. Make the ingredients and directions to be a list instead of just plain text (Done)
4. Make the website responsive (Almost Done)
5. The website design (Done)
6. Add the date when the recipe is created and on the comments section (Done)
7. Deploy on free hosting website (Hosted on glitch.com)


## ADDITIONAL STUFFS TO IMPROVE THE PROJECT ##
1. Create an API so the recipes can be accessed by other applications/website
2. Get data from the API of other websites (Added the random quote generator API (http://quotes.stormconsultancy.co.uk/))

Note: Still learning about API's


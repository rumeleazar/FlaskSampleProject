from flask import Flask, render_template, request, url_for, session, flash, redirect
from flask_mysqldb import MySQL
from datetime import timedelta
#from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'MySecretKey'
app.permanent_session_lifetime = timedelta(hours = 2)
#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:sqlroot123!@localhost/db'
#db = SQLAlchemy(app)

# class User(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(20))
    #password = db.Column(db.password(20))
    #email = db.Column(db.String(20))

#Path to the static folder for image uploading
app.config['STATIC_FOLDER'] = '/Users/rj/Desktop/PythonProjects/static/images/recipeimages' 
app.config['ALLOWED_EXTENSIONS'] = ['PNG', 'JPG', 'JPEG', 'GIF']
 
#File extension checking
def allowed_file(filename):
   
   if not "." in filename:
   		return False 

   ext = filename.rsplit(".", 1)[1]

   if ext.upper() in app.config['ALLOWED_EXTENSIONS']:
   		return True
   else:
   		return False 


 #MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='sqlroot123!'
app.config['MYSQL_DB'] = 'flask'

#Initialize the app for MYSQL
mysql = MySQL(app)


#ROUTE FOR THE HOME
@app.route('/')
@app.route('/<username>')
def home(username = None):

	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM recipe")
	recipe = cur.fetchall()

	if 'username' in session:
		cur = mysql.connection.cursor()
		cur.execute("SELECT firstname FROM user WHERE username = %s ", [username])
		name = cur.fetchall()

		return render_template("index.html", firstname = name , recipe = recipe)

	return render_template("index.html", recipe = recipe)



#ROUTE FOR THE PROFILE TAB
@app.route('/profile/<username>')
def profile(username):

	user = session['username']
	#Showing users own created recipe
	curuser = mysql.connection.cursor()
	curuser.execute("SELECT * FROM recipe WHERE author = %s", [user])
	UsersRecipe = curuser.fetchall()
	
	#Showing users reading list
	curlist = mysql.connection.cursor()
	curlist.execute("SELECT recipe.id, recipe.dishname, recipe.description, recipe.ingredients, recipe.directions, recipe.imagename, recipe.author FROM recipe INNER JOIN readinglist ON recipe.dishname = readinglist.dishname WHERE user = %s", [user])
	UsersReadingList = curlist.fetchall() 

	return render_template('profile.html', UsersRecipe = UsersRecipe, UsersReadingList = UsersReadingList, username = user)

	#USERLIST CAN'T USE THE FETCHALL FUNCTION SINCE IT WILL GIVE THE PROGRAM MULTIPLE ROWS AND THE RECIPENAME AND RECIPEAUTHOR CANNOT RETURN 2 VALUES
	#ANOTHER PROBLEM: RECIPENAME REFERENCE BEFORE ASSIGNMENT 

		#NOTE: PROBLEM SOLVED USING SELECT recipe.dishname, recipe.description, recipe.ingredients, recipe.directions, recipe.imagename, recipe.author FROM recipe INNER JOIN readinglist ON recipe.dishname = readinglist.dishname; 

	#NEW PROBLEM: READING LIST IS ALL SHOWN ON EVERY ACCOUNT(EXAMPLE: USER 1'S READING LIST IS ALSO SAVE IN USER 2'S READING LIST)

	   	#NOTE: PROBLEM SOLVED BY ADDING WHERE ON THE SQL EXECUTE


#ROUTE FOR THE REGISTER TAB
@app.route('/register', methods =['POST','GET'])
def register():
	if request.method == 'POST':
		if request.form['username'] == '' or request.form['password'] == '' or request.form['email'] == '' or request.form['firstname'] == '' or request.form['lastname'] == '':
			flash('Please fill up all the forms')
			return redirect(url_for('register'))
		else:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			firstname = request.form['firstname']
			lastname = request.form['lastname']
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO user(username, password, email, firstname, lastname) VALUES(%s, %s, %s, %s, %s)",(username, password, email, firstname, lastname))
			mysql.connection.commit()
			cur.close()
			flash('Registration Complete')
			return redirect(url_for('home'))

	return render_template('register.html')


#ROUTE FOR THE MODAL LOGIN
@app.route('/login', methods = ['POST', 'GET'])
def login():

	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		session.permanent = True
		username = request.form['username']
		password = request.form['password']
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
		account = cur.fetchone()

		if account:	
			session['loggedin'] = True
			session['username'] = username
			session['password'] = password
			return redirect(url_for('home', username = username))
		else:
			flash('Incorrect Username or Password')
			return redirect(url_for('login'))

	return render_template('login.html')



#ROUTE FOR THE LOGOUT BUTTON
@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('home'))


#ROUTE FOR THE ADD RECIPE FUNCTION
@app.route('/addrecipe', methods = ['POST', 'GET'])
def addrecipe():

	if request.method == 'POST':
		dishname = request.form['dishname']
		description = request.form['description']
		ingredients = request.form['ingredients']
		directions = request.form['directions']
		image = request.files['image']
		author = session['username']

		if not image:
			imagename = 'default.gif'

		if image and not allowed_file(image.filename):
			flash("That image extension is not allowed")
			return redirect('addrecipe')

		else:	
			if image and allowed_file(image.filename):
				imagename = image.filename
				image.save(os.path.join(app.config['STATIC_FOLDER'], imagename))

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO recipe(dishname,description,ingredients,directions,imagename,author) VALUES(%s , %s, %s, %s, %s, %s)",(dishname,description,ingredients, directions,imagename,author))
		mysql.connection.commit()
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM recipe")
		recipe = cur.fetchall()

		if session.get('username', None) is not None:
			return render_template('index.html',recipe = recipe, imagename = imagename)	
		else:
			return render_template('index.html',recipe = recipe, imagename = imagename)

	return render_template('addrecipe.html')

	return render_template('index.html',recipe = recipe, imagename = imagename)



#THIS IS THE WHERE YOU CAN CLICK THE RECIPE AND IT WILL REDIRECT YOU TO THE RECIPE DETAILS
@app.route('/article/<id>', methods = ['POST','GET'])
@app.route('/')
def article(id):

	cur = mysql.connection.cursor()
	cur.execute("SELECT comments, user FROM comments WHERE id = %s",[id])
	comments = cur.fetchall()

	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM recipe WHERE id = %s",[id])
	recipe = cur.fetchall()

	if request.method == 'POST':
		if session['username']:
			comment = request.form['comments']
			user = session['username']
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO comments(comments, id, user) VALUES(%s , %s, %s)",(comment,id, user))
			mysql.connection.commit()
			cur.close()
			cur = mysql.connection.cursor()
			cur.execute("SELECT comments, user FROM comments WHERE id = %s",[id])
			comments = cur.fetchall()

			return render_template('article.html', comments = comments, recipe = recipe)



	return render_template('article.html', recipe = recipe, comments = comments)


#EDIT FUNCTIONALITY OF THE WEBSITE
@app.route('/article/<id>/update', methods = ['POST','GET'])
def update(id):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM recipe WHERE id = %s",[id])
	recipe = cur.fetchone()

	if request.method == 'POST':
		dishname = request.form['dishname']
		description = request.form['description']
		ingredients = request.form['ingredients']
		directions = request.form['directions']
		image = request.files['image']

		if not image:
			imagename = 'default.gif'

		if image and not allowed_file(image.filename):
			flash("That image extension is not allowed")
			return redirect('update')

		else:	
			if image and allowed_file(image.filename):
				imagename = secure_filename(image.filename)
				image.save(os.path.join(app.config['STATIC_FOLDER'], imagename))
			
		
		cur = mysql.connection.cursor()
		cur.execute("UPDATE recipe SET dishname =%s,description =%s,ingredients =%s,directions =%s,imagename =%s WHERE id = %s",(dishname,description,ingredients,directions,imagename,id))
		mysql.connection.commit()
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM recipe WHERE id = %s",[id])
		recipe = cur.fetchall()
		return redirect(url_for('article', recipe = recipe, id = id))

	return render_template('update.html')

#DELETE FUNCTIONALITY OF THE WEBSITE
@app.route('/article/<id>/delete', methods = ['POST','GET'])
def delete(id):
	username = session['username']

	if request.method == 'GET':
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM recipe WHERE id = %s", [id])
		mysql.connection.commit()
		cur.close()
		flash('Recipe has been successfully deleted')
		return redirect(url_for('home', id =id, username = username))

	return redirect(url_for('home', username = username))


#ADD TO READING LIST FUNCTION
@app.route('/article/<id>/addtoreadinglist' , methods = ['POST','GET'])
def addtoreadinglist(id):

	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM recipe WHERE id = %s", [id])
	selectrecipe = cur.fetchone()
	dishname = selectrecipe[1]
	author = selectrecipe[6]
	user = session['username']

	if request.method == 'GET':
		cur = mysql.connection.cursor()
		cur.execute('SELECT dishname FROM readinglist WHERE dishname = %s AND user = %s ',(dishname,user))
		readlist = cur.fetchall()
		
		if readlist:
			for recipe in readlist:
					if dishname in recipe[0]:
						return redirect(url_for('profile', id = id, username = user))
					else:
						cur = mysql.connection.cursor()
						cur.execute("INSERT INTO readinglist(dishname, author, user) VALUES(%s, %s, %s)", (dishname, author, user))
						mysql.connection.commit()
						cur.close()
						return redirect(url_for('profile', id = id, username = user))
		else:
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO readinglist(dishname, author, user) VALUES(%s, %s, %s)", (dishname, author, user))
			mysql.connection.commit()
			cur.close()
						

	return redirect(url_for('profile', id = id, username = user))


		#NOTE: ADD THAT IF A RECIPE IS ALREADY IN THE READING LIST, DON'T WRITE IT AGAIN ON THE DATABASE

		#PROBLEM: USER CAN ONLY ADD HIS OWN RECIPE TO THE READING LIST

		#PROBLEM IS SOLVED


#REMOVE TO READING LIST FUNCTION
@app.route('/article/<id>/removefromreadinglist', methods = ['GET'])
def removefromreadinglist(id):

	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM recipe WHERE id = %s", [id])
	selectrecipe = cur.fetchone()
	dishname = selectrecipe[1]
	author = selectrecipe[6]
	user = session['username']

	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM readinglist WHERE dishname = %s", [dishname])
	selectrecipe = cur.fetchone()

	if request.method == 'GET':

		if selectrecipe:
			cur = mysql.connection.cursor()
			cur.execute("DELETE FROM readinglist WHERE dishname = %s", [dishname])
			mysql.connection.commit()
			cur.close()

		return redirect(url_for('profile', id = id, username = user, selectrecipe = selectrecipe))

#PROBLEM: HOW TO ISOLATE THE REMOVE FROM READING LIST BUTTON TO THOSE WHO ARE THE ONLY ONES TO ADD THE RECIPE TO HIS/HER READING LIST



if __name__ == '__main__':
   app.run(debug = True)
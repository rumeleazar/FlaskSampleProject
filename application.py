from flask import Flask, render_template, request, url_for, session, flash, redirect
# from flask_mysqldb import MySQL
from datetime import timedelta
import os
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = 'MySecretKey'
app.permanent_session_lifetime = timedelta(hours=2)
app.config['STATIC_FOLDER'] = '/Users/rj/Desktop/PythonProjects/static/images/recipeimages'
app.config['ALLOWED_EXTENSIONS'] = ['PNG', 'JPG', 'JPEG', 'GIF']

# File extension checking


def allowed_file(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config['ALLOWED_EXTENSIONS']:
        return True
    else:
        return False

 # MySQL Config
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] ='sqlroot123!'
# app.config['MYSQL_DB'] = 'flask'

# #Initialize the app for MYSQL
# mysql = MySQL(app)


# ROUTE FOR THE HOME
@app.route('/')
@app.route('/<username>')
def home(username=None):
    # SQLITE3 COMMANDS:
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipe")
        recipe = cur.fetchall()

  # MYSQL COMMANDS:
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM recipe")
    # recipe = cur.fetchall()

    if 'username' in session:
        cur = conn.cursor()
        # cur = mysql.connection.cursor()
        cur.execute(
            "SELECT firstname FROM user WHERE username = ?", [username])
        name = cur.fetchall()

        return render_template("index.html", firstname=name, recipe=recipe)

    return render_template("index.html", recipe=recipe)


# ROUTE FOR THE PROFILE TAB
@app.route('/profile/<username>')
def profile(username):

    with sqlite3.connect('database.db') as conn:
        user = session['username']
        # Showing users own created recipe
        curuser = conn.cursor()
        curuser.execute("SELECT * FROM recipe WHERE author = ?", [user])
        UsersRecipe = curuser.fetchall()

    # Showing users reading list
        curlist = conn.cursor()
        curlist.execute(
            "SELECT recipe.id, recipe.dishname, recipe.description, recipe.ingredients, recipe.directions, recipe.imagename, recipe.author FROM recipe INNER JOIN readinglist ON recipe.dishname = readinglist.dishname WHERE user = ?", [user])
        UsersReadingList = curlist.fetchall()

        return render_template('profile.html', UsersRecipe=UsersRecipe, UsersReadingList=UsersReadingList, username=user)

    # USERLIST CAN'T USE THE FETCHALL FUNCTION SINCE IT WILL GIVE THE PROGRAM MULTIPLE ROWS AND THE RECIPENAME AND RECIPEAUTHOR CANNOT RETURN 2 VALUES
    # ANOTHER PROBLEM: RECIPENAME REFERENCE BEFORE ASSIGNMENT

        # NOTE: PROBLEM SOLVED USING SELECT recipe.dishname, recipe.description, recipe.ingredients, recipe.directions, recipe.imagename, recipe.author FROM recipe INNER JOIN readinglist ON recipe.dishname = readinglist.dishname;

    # NEW PROBLEM: READING LIST IS ALL SHOWN ON EVERY ACCOUNT(EXAMPLE: USER 1'S READING LIST IS ALSO SAVE IN USER 2'S READING LIST)

        # NOTE: PROBLEM SOLVED BY ADDING WHERE ON THE SQL EXECUTE


# ROUTE FOR THE REGISTER TAB
@app.route('/register', methods=['POST', 'GET'])
def register():
    with sqlite3.connect('database.db') as conn:
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
                cur = conn.cursor()
                cur.execute("INSERT INTO user(username, password, email, firstname, lastname) VALUES(?, ?, ?, ?, ?)",
                            (username, password, email, firstname, lastname))
                # mysql.connection.commit()
                conn.commit()
                cur.close()
                flash('Registration Complete')
                return redirect(url_for('home'))

        return render_template('register.html')


# ROUTE FOR THE MODAL LOGIN
@app.route('/login', methods=['POST', 'GET'])
def login():

    with sqlite3.connect('database.db') as conn:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            session.permanent = True
            username = request.form['username']
            password = request.form['password']
            # cur = mysql.connection.cursor()
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
            account = cur.fetchone()

            if account:
                session['loggedin'] = True
                session['username'] = username
                session['password'] = password
                return redirect(url_for('home', username=username))
            else:
                flash('Incorrect Username or Password')
                return redirect(url_for('login'))

        return render_template('login.html')


# ROUTE FOR THE LOGOUT BUTTON
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


# ROUTE FOR THE ADD RECIPE FUNCTION
@app.route('/addrecipe', methods=['POST', 'GET'])
def addrecipe():


    #PROBLEM WITH THE INGREDIENTS SPLIT
    with sqlite3.connect('database.db') as conn:
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
                    image.save(os.path.join(
                        app.config['STATIC_FOLDER'], imagename))

            cur = conn.cursor()
            cur.execute("INSERT INTO recipe(dishname,description,ingredients,directions,imagename,author) VALUES(? , ?, ?, ?, ?, ?)",
                        (dishname, description, ingredients, directions, imagename, author))
            conn.commit()
            cur = conn.cursor()
            cur.execute("SELECT * FROM recipe")
            recipe = cur.fetchall()

            if session.get('username', None) is not None:
                return render_template('index.html', recipe=recipe, imagename=imagename)
            else:
                return render_template('index.html', recipe=recipe, imagename=imagename)

        return render_template('addrecipe.html')

        return render_template('index.html', recipe=recipe, imagename=imagename)


# THIS IS THE WHERE YOU CAN CLICK THE RECIPE AND IT WILL REDIRECT YOU TO THE RECIPE DETAILS
@app.route('/article/<id>', methods=['POST', 'GET'])
@app.route('/')
def article(id):

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT comments, user FROM comments WHERE id = ?", [id])
        comments = cur.fetchall()

        cur = conn.cursor()
        cur.execute("SELECT * FROM recipe WHERE id = ?", [id])
        recipe = cur.fetchall()

        if request.method == 'POST':
            if session['username']:
                comment = request.form['comments']
                user = session['username']
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO comments(comments, id, user) VALUES(?,?,?)", (comment, id, user))
                conn.commit()
                cur.close()
                cur = conn.cursor()
                cur.execute(
                    "SELECT comments, user FROM comments WHERE id = ?", [id])
                comments = cur.fetchall()

                return render_template('article.html', comments=comments, recipe=recipe)

        return render_template('article.html', recipe=recipe, comments=comments)

    return render_template('article.html', recipe=recipe, comments=comments)


    


# EDIT FUNCTIONALITY OF THE WEBSITE
@app.route('/article/<id>/update', methods=['POST', 'GET'])
def update(id):

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipe WHERE id = ?", [id])
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
                    image.save(os.path.join(
                        app.config['STATIC_FOLDER'], imagename))

            cur = conn.cursor()
            cur.execute("UPDATE recipe SET dishname =?,description =?,ingredients =?,directions =?,imagename =? WHERE id =?",
                        (dishname, description, ingredients, directions, imagename, id))
            conn.commit()
            cur = conn.cursor()
            cur.execute("SELECT * FROM recipe WHERE id = ?", [id])
            recipe = cur.fetchall()
            return redirect(url_for('article', recipe=recipe, id=id))

        return render_template('update.html')

# DELETE FUNCTIONALITY OF THE WEBSITE
@app.route('/article/<id>/delete', methods=['POST', 'GET'])
def delete(id):
    username = session['username']

    with sqlite3.connect('database.db') as conn:

        if request.method == 'GET':
            cur = conn.cursor()
            cur.execute("DELETE FROM recipe WHERE id = ?", [id])
            conn.commit()
            cur.close()
            flash('Recipe has been successfully deleted')
            return redirect(url_for('home', id=id, username=username))

        return redirect(url_for('home', username=username))


# ADD TO READING LIST FUNCTION
@app.route('/article/<id>/addtoreadinglist', methods=['POST', 'GET'])
def addtoreadinglist(id):

    with sqlite3.connect('database.db') as conn:

        cur = conn.cursor()
        cur.execute("SELECT * FROM recipe WHERE id = ?", [id])
        selectrecipe = cur.fetchone()
        dishname = selectrecipe[1]
        author = selectrecipe[6]
        user = session['username']

        if request.method == 'GET':
            cur = conn.cursor()
            cur.execute(
                'SELECT dishname FROM readinglist WHERE dishname = ? AND user = ? ', (dishname, user))
            readlist = cur.fetchall()

            if readlist:
                for recipe in readlist:
                    if dishname in recipe[0]:
                        return redirect(url_for('profile', id=id, username=user))
                    else:
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO readinglist(dishname, author, user) VALUES(?, ?, ?)", (dishname, author, user))
                        conn.commit()
                        cur.close()
                        return redirect(url_for('profile', id=id, username=user))
            else:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO readinglist(dishname, author, user) VALUES(?, ?, ?)", (dishname, author, user))
                conn.commit()
                cur.close()

        return redirect(url_for('profile', id=id, username=user))

        # NOTE: ADD THAT IF A RECIPE IS ALREADY IN THE READING LIST, DON'T WRITE IT AGAIN ON THE DATABASE

        # PROBLEM: USER CAN ONLY ADD HIS OWN RECIPE TO THE READING LIST

        # PROBLEM IS SOLVED


# REMOVE TO READING LIST FUNCTION
@app.route('/article/<id>/removefromreadinglist', methods=['GET'])
def removefromreadinglist(id):

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipe WHERE id = ?", [id])
        selectrecipe = cur.fetchone()
        dishname = selectrecipe[1]
        author = selectrecipe[6]
        user = session['username']

        cur = conn.cursor()
        cur.execute("SELECT * FROM readinglist WHERE dishname = ?", [dishname])
        selectrecipe = cur.fetchone()

        if request.method == 'GET':

            if selectrecipe:
                cur = conn.cursor()
                cur.execute(
                    "DELETE FROM readinglist WHERE dishname = ?", [dishname])
                conn.commit()
                cur.close()

            return redirect(url_for('profile', id=id, username=user, selectrecipe=selectrecipe))

# PROBLEM: HOW TO ISOLATE THE REMOVE FROM READING LIST BUTTON TO THOSE WHO ARE THE ONLY ONES TO ADD THE RECIPE TO HIS/HER READING LIST


if __name__ == '__main__':
    app.run(debug=True)

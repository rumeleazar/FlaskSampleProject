from flask import Flask, render_template, request, url_for, session, flash, redirect
from datetime import timedelta, date
import os
from werkzeug.utils import secure_filename
import sqlite3
import json
import requests

app = Flask(__name__)
app.secret_key = 'MySecretKey'
app.permanent_session_lifetime = timedelta(hours=2)
app.config['STATIC_FOLDER'] = 'static/images/recipeimages'   # /Users/rj/Desktop/PythonProjects
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


# ROUTE FOR THE HOME
@app.route('/' , methods = ['POST', 'GET'])
@app.route('/<username>', methods = ['POST', 'GET'])
def home(username=None):

    #Random Quote Simulator API
    r = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    content = r.text
    content = json.loads(content)
    quote = content["quote"]
    author = content["author"]


    if request.method == 'POST':
        recipe = request.form['recipesearch']
        
        return search(recipe)


    # SQLITE3 COMMANDS:
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipe")
        recipe = cur.fetchall()

    if 'username' in session:
        cur = conn.cursor()
        cur.execute(
            "SELECT firstname FROM user WHERE username = ?", [username])
        name = cur.fetchall()

        return render_template("index.html", firstname=name, recipe=recipe,quote = quote, author = author)

    return render_template("index.html", recipe=recipe,quote = quote, author = author)


# ROUTE FOR THE PROFILE TAB
@app.route('/profile/<username>')
def profile(username):

    with sqlite3.connect('database.db') as conn:
        user = session['username']
        # Showing users own created recipe
        currecipe = conn.cursor()
        currecipe.execute("SELECT * FROM recipe WHERE author = ?", [user])
        UsersRecipe = currecipe.fetchall()

        # Get the Name of the USER
        curuser = conn.cursor()
        curuser.execute("SELECT firstname,lastname FROM user WHERE username = ?",[user])
        UsersName = curuser.fetchall()


        # Showing users reading list
        curlist = conn.cursor()
        curlist.execute(
            "SELECT recipe.id, recipe.dishname, recipe.description, recipe.ingredients, recipe.directions, recipe.imagename, recipe.author FROM recipe INNER JOIN readinglist ON recipe.dishname = readinglist.dishname WHERE user = ?", [user])
        UsersReadingList = curlist.fetchall()

        return render_template('profile.html', UsersRecipe=UsersRecipe, UsersReadingList=UsersReadingList, username=user, UsersName = UsersName)


@app.route('/about')
def about():

    return render_template('about.html')

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
                conn.commit()
                cur.close()
                flash('Registration Complete')
                return redirect(url_for('home'))

        return render_template('register.html')


        #MAKE AN IF STATEMENTS THAT WILL TELL THE USER IF THE USERNAME IS ALREADY TAKEN


# ROUTE FOR THE LOGIN
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
            dateformat = date.today()
            datetoday = dateformat.strftime("%B %d, %Y")

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
            cur.execute("INSERT INTO recipe(dishname,description,ingredients,directions,imagename,author,datetoday) VALUES(? , ?, ?, ?, ?, ?,?)",
                        (dishname, description, ingredients, directions, imagename, author, datetoday))
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
@app.route('/article/<id>/<dishname>', methods=['POST', 'GET'])
@app.route('/')
def article(id,dishname):


    with sqlite3.connect('database.db') as conn:    
        cur = conn.cursor()
        cur.execute("SELECT recipe.dishname, user.firstname, user.lastname, recipe.imagename, recipe.description, recipe.ingredients, recipe.directions,recipe.id,recipe.author,recipe.datetoday FROM recipe INNER JOIN user ON recipe.author = user.username WHERE recipe.id = ?", [id])
        recipe = cur.fetchall()

        cur = conn.cursor()
        cur.execute("SELECT user.firstname, user.lastname, comments.comments,comments.datetoday FROM user INNER JOIN comments ON user.username = comments.user WHERE comments.id = ?",[id])
        usercomment = cur.fetchall()

        if request.method == 'POST':
            if session['username']:
                comment = request.form['comments']
                user = session['username']
                dateformat = date.today()
                datetoday = dateformat.strftime("%B %d, %Y")
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO comments(comments, id, user,datetoday) VALUES(?,?,?,?)", (comment, id, user, datetoday))
                conn.commit()
                cur.close()

                cur = conn.cursor()
                cur.execute("SELECT user.firstname, user.lastname, comments.comments,comments.datetoday FROM user INNER JOIN comments ON user.username = comments.user WHERE comments.id = ?",[id])
                usercomment = cur.fetchall()
                
                return render_template('article.html', recipe=recipe, usercomment = usercomment)

    return render_template('article.html', recipe=recipe, usercomment = usercomment)


    


# EDIT FUNCTIONALITY OF THE WEBSITE
@app.route('/article/<id>/<dishname>/update', methods=['POST', 'GET'])
def update(id,dishname):

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipe WHERE id = ?", [id])
        recipe = cur.fetchall()

        if request.method == 'POST':
            dishname = request.form['dishname']
            description = request.form['description']
            ingredients = request.form['ingredients']
            directions = request.form['directions']
            image = request.files['image']

            if not image:
                for x in recipe:
                    imagename = x[5]

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

        return render_template('update.html', recipe = recipe)

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


@app.route('/search/<recipe>')
def search(recipe):

    recipe = '%' + recipe + '%'
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipe WHERE dishname LIKE ?", [recipe])
        recipe = cur.fetchall()

        return render_template('search.html', recipe = recipe)


# @app.route('/admin')
# def admin():
    



if __name__ == '__main__':
    app.run(debug=True)

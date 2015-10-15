from flask import Flask, render_template, session, request
from flask import redirect, url_for
import sqlite3
import utils

app = Flask(__name__)

@app.route("/about")
def about():
        return render_template("about.html")
        
@app.route("/login", methods = ['GET','POST'])
def login():
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        q = "SELECT users.name FROM users"
        cur.execute(q)
        all_rows = cur.fetchall()
        print all_rows
        if request.method == 'POST':
                user = str(request.form['user'])
                password = str(request.form['pass'])
                if utils.authenticate(user,password):
                        session['user'] = utils.getUserId(user)
                        return redirect("/home")
                else:
                        return render_template("login.html")
        return render_template("login.html") #login failed

@app.route("/home")
def home():
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        q = "SELECT posts.content,posts.pid,posts.uid,users.name,posts.title FROM posts, users WHERE users.id = posts.uid ORDER BY posts.pid DESC"
        cur.execute(q)
        all_rows = cur.fetchall()
        print all_rows
        return render_template("home.html", all_rows=all_rows)

@app.route("/post/<int:postid>")
def post(postid):
        postrow = utils.getPost(postid)
        commentrow = utils.getCommentsOnPost(postid)
        print commentrow
        return render_template("post.html", postrow = postrow, commentrow = commentrow)

@app.route("/makepost", methods = ['GET','POST'])
def makepost():
        if 'user' not in session:
                return redirect ("/home")
        if request.method == 'POST':
                title = request.form['title']
                content = request.form['content']
                user = session['user']
                idp = utils.writePost(title,content,user)
                return redirect("/post/"+str(idp))
        else:
                return render_template("newpost.html")

@app.route("/")
def index():
        return "hello"
        
if __name__ == "__main__":
        app.secret_key = "hello"
        app.debug = True
        app.run(host='0.0.0.0', port=8000)
        #app.run(debug=True)
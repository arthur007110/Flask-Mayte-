import os
import os.path
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

DATABASE = "users.db"

app = Flask(__name__)

app.config.from_object(__name__)

app.config.update(dict(
DATABASE = os.path.join(app.root_path,'users.db'),
SECRET_KEY ='development key',
USERNAME ='admin',
PASSWORD ='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent = True)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('flaskDB.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def register_db(username, email, password):
    db = get_db()
    params = (query_db('SELECT COUNT(*) FROM users')[0][0]+1, username, email, password)
    query = db.execute('INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?);', (params),)
    db.commit() 
    query.fetchall()

def login_db(username, password):
    db = get_db()
    select = f'SELECT * FROM users WHERE username = "{username}" AND password = "{password}"'
    result = query_db(select)
    db.commit()
    if(result == []):
        return False
    else:
        return True
        

@app.route('/register', methods = ["GET", "POST"])      
def register():
    if request.method == "POST":
        
        register_db(request.form['username'], request.form['email'], request.form['password'])
        
        return '<h1>Registered</h1><br> <a href="/login">Voltar</a>'
    
    return render_template('register.html')

@app.route('/login', methods = ["GET", "POST"])      
def login():
    if request.method == "POST":
        
        if(login_db(request.form['username'], request.form['password'])):
            return '<h1>Sucessfull Login</h1><br> <a href="/login">Voltar</a>'
        else:
            return '<h1>Bad Login, Try Again</h1><br> <a href="/login">Voltar</a>'
        
    return render_template('login.html')

with app.app_context():
    app.run(use_reloader = True)
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3
import os
from app import app
import random
from random import randint


app.config.from_object(__name__)
DATABASE = "users.db"

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
        
def register_user(username, email, password):
    db = get_db()
    id = random_id()
    insert = f'INSERT INTO users (id, username, email, password) VALUES ({id}, "{username}", "{email}", "{password}")'
    query_db(insert)
    db.commit()
    return True

def login_user(username, password):
    db = get_db()
    select = f'SELECT * FROM users WHERE username = "{username}" AND password = "{password}"'
    result = query_db(select)
    db.commit()
    if(result == []):
        return False
    else:
        return result[0][0]

def update_user(id, username, email, password):
    db = get_db()
    select = f'UPDATE users SET username = "{username}", email = "{email}", password = "{password}" WHERE id = "{id}";'
    query_db(select)
    db.commit()
    return True

def delete_user(id):
    db = get_db()
    delete = f'DELETE FROM users WHERE id = "{id}";'
    query_db(delete)
    db.commit()
    return True

def get_user(id):
    db = get_db()
    select = f'SELECT * FROM users WHERE id = "{id}"'
    result = query_db(select)
    db.commit()
    if(result == []):
        return False
    else:
        return result[0]

def get_users():
    db = get_db()
    select = f'SELECT * FROM users'
    result = query_db(select)
    db.commit()
    if(result == []):
        return []
    else:
        return result
    
def random_id(id_length = 8):
    range_start = 10**(id_length-1)
    range_end = (10**id_length)-1
    return randint(range_start, range_end)

def printUsers():
    print(query_db('SELECT * FROM users'))
        
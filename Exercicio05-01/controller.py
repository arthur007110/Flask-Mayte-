from app import app
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from model import register_user, login_user, update_user, delete_user, get_user, get_users

@app.route('/main/<id>/', methods = ["GET", "POST"])
def main(id):
    if(request.method == "POST"):
        if(request.form['option_button'] == "Update"):
            return redirect(url_for('update', id = id))
        elif(request.form['option_button'] == "Delete"):
            return redirect(url_for('delete', id = id))
        elif(request.form['option_button'] == "Display"):
            return redirect(url_for('display', id = id))
        elif(request.form['option_button'] == "Display All"):
            return redirect(url_for('display_all'))
        
    return render_template('main.html')

@app.route('/register/', methods = ["GET", "POST"])      
def register():
    if request.method == "POST":
        if(register_user(request.form['username'], request.form['email'], request.form['password'])):
            return '<h1>Registered</h1><br> <a href="/login">Voltar</a>'
        else:
            return '<h1>Something Wrong</h1><br> <a href="/login">Voltar</a>'
    return render_template('register.html')

@app.route('/login/', methods = ["GET", "POST"])      
def login():
    if request.method == "POST":
        user_id = login_user(request.form['username'], request.form['password'])
        if(user_id):
            return redirect(url_for('main', id = user_id))
        else:
            return '<h1>Bad Login, Try Again</h1><br> <a href="/login">Voltar</a>'
        
        
    return render_template('login.html')

@app.route('/update/<id>/', methods = ["GET", "POST"])
def update(id):
    if request.method == "POST":
        if update_user(id, request.form['username'], request.form['email'], request.form['password']):
            return '<h1>Updated</h1><br> <a href="/login">Voltar</a>'
        else:
            return '<h1>Something Wrong</h1><br> <a href="/login">Voltar</a>'
        
    
    return render_template('update.html')

@app.route('/delete/<id>/', methods = ["GET"])
def delete(id):
    if delete_user(id):
        return '<h1>Deleted</h1><br> <a href="/login">Voltar</a>'
    else:
        return '<h1>Something Wrong</h1><br> <a href="/login">Voltar</a>'
    
@app.route('/display/<id>/', methods = ["GET"])
def display(id):
    user = get_user(id)
    if user:
        return f'<h1>View User</h1><br> username: {user[1]}<br> email: {user[2]}<br> <a href="/main/{id}">Voltar</a>'
    else:
        return '<h1>Something Wrong</h1><br> <a href="/main/{id}">Voltar</a>'
    
@app.route('/displayAll/', methods = ["GET"])
def display_all():
    users = get_users()
    view = f'<h1>View Users</h1><br>'
    if users == []:
        return '<h1>Something Wrong</h1><br> <a href="/main/{id}">Voltar</a>'
    for user in users:
        view += f'ID: {user[0]}<br> User: {user[1]}<br> Email: {user[2]}<br> Password: {user[3]}<br><br>'
    view += f'<a href="/main/{id}">Voltar</a>'
    return view
        

app.run(use_reloader = True)
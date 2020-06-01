from flask import Flask

app = Flask(__name__)

@app.route("/login")
def login():
    return '<h1>Hello World</h1>'

app.run(use_reloader = True)
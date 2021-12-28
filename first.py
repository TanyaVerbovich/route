from collections import namedtuple
from flask import Flask, render_template, redirect, url_for, request, g, flash
import sqlite3
import os
import re
import hashlib
from FDataBase import FDataBase

DATABASE = '/tmp/flsite.db'
SECRET_KEY = '6nT9Nm6nT9Nm6nT9Nm'

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def hashPassword(password):
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()

def connect_db():
#connect to database
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
#create database via request into python console
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/', methods=['GET'])
#page index
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu())


@app.route('/main', methods=['GET'])
#main page
def main():
    return render_template('main.html')


@app.route('/signin', methods=['GET'])
#signin page
def signin():
    return  render_template('signin.html')


@app.route('/register', methods=['POST', 'GET'])
#register page
def register():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        # requirements for password: not less than 8 symbols, should include a-z 0-9 special symbol
        if re.match(r'^.*(?=.{6,})(?=.*[a-z])(?=.*[!@#$%^&*?_]).*$', request.form['password']):
            res = dbase.addUser(request.form['username'], hashPassword(request.form['password']), request.form['email'],
                                request.form['role'])
            if not res:
                flash('error while adding user', category='error')
            else:
                flash('added successfully', category='success')
        else:
            flash('your password is incorrect', category='error')

    return render_template('register.html', menu=dbase.getMenu())




@app.route('/adduser', methods=['POST', 'GET'])
#adding user into database table users
def addUser():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        # requirements for password: not less than 8 symbols, should include A-Z a-z 0-9 special symbol
        if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', request.form['password']):
            res = dbase.addUser(request.form['username'], hashPassword(request.form['password']), request.form['email'],
                                request.form['role'])
            if not res:
                flash('error while adding user', category='error')
            else:
                flash('added successfully', category='success')
        else:
            flash('your password is incorrect', category='error')

    return render_template('add_user.html', menu=dbase.getMenu())


if __name__ == "__main__":
    app.run()

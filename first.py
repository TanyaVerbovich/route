from flask import Flask, render_template, redirect, url_for, request, g, flash, session
from flask_session import Session
import sqlite3
import os
import re
import hashlib
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///route.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'
sess = Session()


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username


def hashPassword(password):
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()


@app.route('/', methods=['POST', 'GET'])
#page index
def index():
    return render_template('index.html')


@app.route('/main', methods=['POST', 'GET'])
#main page
def main():
    return render_template('main.html')


@app.route('/signin', methods=['POST', 'GET'])
#signin page
def signin():
    if request.method == "POST":
        curruser = User.query.filter_by(username=request.form['username']).first()
        if curruser is None:
            flash('there is no such user')
        else:
            if curruser.password == hashPassword(request.form['password']):
                return redirect(url_for('main'))
            else:
                flash('incorrect data', category='error')

    return  render_template('signin.html')


@app.route('/register', methods=['POST', 'GET'])
#register page
def register():
    if request.method == "POST":
        # requirements for password: not less than 8 symbols, should include a-z 0-9 special symbol
        curuser = User.query.filter_by(username=request.form['username']).first()
        curemail = User.query.filter_by(username=request.form['email']).first()
        if curuser is None and curemail is None:
            if re.match(r'^.*(?=.{6,})(?=.*[a-z])(?=.*[!@#$%^&*?_]).*$', request.form['password']):
                try:
                    u = User(username=request.form['username'], password=hashPassword(request.form['password']),
                             email=request.form['email'], role=request.form['role'], start_date=date.today())
                    db.session.add(u)
                    db.session.flush()
                    db.session.commit()
                    flash('added successfully', category='success')
                except:
                    db.session.rollback()
                    flash('error while adding into database', category='error')
            else:
                flash('your password is incorrect', category='error')
        else:
            flash('user is not unique', category='error')

    return render_template('register.html')


if __name__ == "__main__":
    app.run()

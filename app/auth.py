from app import app, db
from flask import request, redirect, url_for, render_template, flash, session
from app.models import User, create_tables
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.execute(text('SELECT * FROM user WHERE username = :username'), {'username':username}).fetchone()
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password','danger')
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = db.session.execute(text('SELECT * FROM user WHERE username = :username'), {'username':username}).fetchone()
        if user:
            flash('Username already taken','danger')
        else:
            query = text('INSERT INTO user (username, password) VALUES (:username, :password)')
            db.session.execute(query, {'username': username, 'password': hashed_password})
            flash('Registration successful! You can now login', "success")
            return redirect(url_for('login'))
    return render_template('register.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))
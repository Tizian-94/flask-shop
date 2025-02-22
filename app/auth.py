from app import app, db
from flask import request, redirect, url_for, render_template, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

@app.before_request
def load_logged_in_user():
    username = session.get('username')
    if username is None:
        g.user = None
    else:
        user = db.session.execute(text('SELECT * FROM user WHERE username = :username'), {'username': username}).fetchone()
        g.user = user

@app.context_processor
def inject_user():
    return {'user': g.user}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.execute(text('SELECT * FROM user WHERE username = :username'), {'username': username}).fetchone()
        if user:
            db_password = user[2]
            if check_password_hash(db_password, password):
                session['username'] = user[1]
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'danger')
        else:
            flash('User not found', 'danger')
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = db.session.execute(text('SELECT * FROM user WHERE username = :username'), {'username': username}).fetchone()
        if user:
            flash('Username already taken', 'danger')
        else:
            query = text('INSERT INTO user (username, password, isadmin) VALUES (:username, :password, :isadmin)')
            db.session.execute(query, {'username': username, 'password': hashed_password, 'isadmin': False})
            db.session.commit()
            flash('Registration successful! You can now login', "success")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.before_request
def load_logged_in_user():
    username = session.get('username')
    if username is None:
        g.user = None
        print("No user logged in.")
    else:
        user = db.session.execute(text('SELECT * FROM user WHERE username = :username'), {'username': username}).fetchone()
        g.user = user
        print(f"Logged in user: {g.user}")

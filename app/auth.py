from app import app
from flask import request, redirect, url_for, render_template, flash, session

users = {
    'user1':'password1',
    'user2':'password2'
}

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
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
        if username in users:
            flash('Username already taken','danger')
        else:
            users[username] = password
            flash('Registration successful! You can now login', "success")
            return redirect(url_for('login'))
    
    return render_template('register.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))
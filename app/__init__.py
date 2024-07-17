import os
from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SECRET_KEY"] = '?O(8k"@AUia=*F5c?}?o(TbZ%JjKhp'

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'site.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import routes, auth, models

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

@app.context_processor
def cart_item_count():
    if 'username' in session:
        user = db.session.execute(text('SELECT * FROM user WHERE username = :username'), {'username': session['username']}).fetchone()
        if user:
            cart_items = db.session.execute(text('SELECT SUM(quantity) FROM cart_item WHERE user_id = :user_id'), {'user_id': user.id}).fetchone()
            cart_count = cart_items[0] if cart_items[0] else 0
            return {'cart_item_count': cart_count}
    return {'cart_item_count': 0}

if __name__ == '__main__':
    app.run(debug=True)

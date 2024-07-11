import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask (__name__)
app.config["SECRET_KEY"] = '?O(8k"@AUia=*F5c?}?o(TbZ%JjKhp'

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'site.db')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import routes, auth, models

@app.context_processor
def cart_item_count():
    if 'username' in session:
        user = db.session.execute(text('SELECT * FROM user WHERE username = :username'), {'username': session['username']}).fetchone()
        if user:
            cart_items = db.session.execute(text('SELECT SUM(quantity) FROM cart_item WHERE user_id= :user_id'), {'user_id':user.id}).fetchone()
            cart_count = cart_items[0] if cart_items[0] else 0
            return {'cart_item_count': cart_count}
        return {'cart_item_count': 0}
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config["SECRET_KEY"] = '?O(8k"@AUia=*F5c?}?o(TbZ%JjKhp'

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'site.db')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import routes, auth, models
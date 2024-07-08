from datetime import datetime
from app import db
from sqlalchemy import text

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime)
    isadmin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.date_created}),"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), nullable=False)
    item_description = db.Column(db.String(200), nullable=False)
    added_by = db.Column(db.String(20), nullable=False) 

    def __repr__(self):
        return f"Items('{self.item_name}', '{self.item_description}', '{self.added_by}')"

    
def create_tables():
    with db.engine.connect() as connection:

        connection.execute(text('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                isadmin BOOLEAN DEFAULT FALSE
            )
        ''')
        )
        
        connection.execute(text('''
            CREATE TABLE IF NOT EXISTS  items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                item_description TEXT NOT NULL,
                added_by TEXT NOT NULL,
            )
        ''')
        )
    db.session.commit()
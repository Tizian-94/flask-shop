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
    image_url = db.Column(db.String(200))
    price = db.Column(db.Float)

    def __repr__(self):
        return f"Item('{self.item_name}', '{self.item_description}', '{self.added_by}', '{self.image_url}', '{self.price}')"

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    item = db.relationship('Item',backref='cart_items')
    user = db.relationship('User',backref='cart_items')

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(20), nullable=False)

    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


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

        connection.execute(text('''
            CREATE TABLE IF NOT EXISTS cart_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (item_id) REFERENCES item(id)
            )
        ''')
        )
    db.session.commit()
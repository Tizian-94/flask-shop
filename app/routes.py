from app import app, db
from flask import request, redirect, render_template, url_for, flash, session
from app.models import Item, User

@app.route('/')
def home():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/admin/add_item', methods=['GET', 'POST'])
def add_item():
    if 'username' not in session:
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    current_user = User.query.filter_by(username=session['username']).first()
    
    if not current_user or not current_user.isadmin:
        flash('You do not have admin permission', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        
        new_item = Item(item_name=item_name, item_description=item_description, added_by=current_user.username)
        db.session.add(new_item)
        db.session.commit()

        flash('Item added successfully!','success')
        return redirect(url_for('home'))
    
    return render_template('add_item.html')
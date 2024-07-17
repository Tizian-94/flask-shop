from app import app, db
from flask import request, redirect, render_template, url_for, flash, session, abort
from app.models import Item, User, CartItem, OrderItem, Order
from sqlalchemy import text
from flask import jsonify

@app.route('/')
def home():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/admin', methods=['GET'])
def admin():
    if 'username' not in session:
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    user = db.session.execute(text('SELECT * FROM user WHERE username = :username'), {'username':session['username']}).fetchone()
    if not user or not user[4]:
        flash('You do not have admin permission to access this page', 'danger')
        return redirect(url_for('home'))
    
    items = Item.query.all()
    
    return render_template('admin.html', items=items)

@app.route('/admin/grant', methods=["POST"])
def grant_admin():
    if 'username' not in session:
        flash('You need to be logged in to access this page', 'danger')
        return redirect(url_for('login'))
    
    current_user = User.query.filter_by(username=session['username']).first()

    if not current_user or not current_user.isadmin:
        flash('You do not have admin permission', 'danger')
        return redirect(url_for('home'))
    
    username = request.form['username']
    user_to_grant = User.query.filter_by(username=username).first()

    if not user_to_grant:
        flash(f'User {username} does not exist.', 'danger')
    elif user_to_grant.isadmin:
        flash(f'User {username} already has admin privileges','danger')
    else:
        user_to_grant.isadmin = True
        db.session.commit()
        flash(f'User {username} has been granted admin privileges', 'success')
    
    return redirect(url_for('admin'))

@app.route('/admin/revoke', methods=["POST"])
def revoke_admin():
    if 'username' not in session:
        flash('You need to be logged in to access this page', 'danger')
        return redirect(url_for('login'))
    
    current_user = User.query.filter_by(username=session['username']).first()

    if not current_user or not current_user.isadmin:
        flash('You do not have admin permission', 'danger')
        return redirect(url_for('home'))
    
    username = request.form['username']
    user_to_revoke = User.query.filter_by(username=username).first()

    if not user_to_revoke:
        flash(f'User {username} does not exist', 'danger')
    elif not user_to_revoke.isadmin:
        flash(f'User {username} does not have admin privileges', 'danger')
    else:
        user_to_revoke.isadmin = False
        db.session.commit()
        flash(f'User {username} has been revoked admin privileges', 'success')

    return redirect(url_for('admin'))


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
        image_url = request.form['image_url']
        price = request.form['price']
        
        new_item = Item(item_name=item_name, item_description=item_description, image_url=image_url, price=price, added_by=current_user.username)
        db.session.add(new_item)
        db.session.commit()

        flash('Item added successfully!','success')
        return redirect(url_for('home'))
    
    return render_template('add_item.html')

@app.route('/admin/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'username' not in session:
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    current_user = User.query.filter_by(username=session['username']).first()
    
    if not current_user or not current_user.isadmin:
        flash('You do not have admin permission', 'danger')
        return redirect(url_for('home'))
    
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.item_name = request.form['item_name']
        item.item_description = request.form['item_description']
        item.image_url = request.form['image_url']
        item.price = request.form['price']
        
        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('edit_item.html', item=item)

@app.route('/admin/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'username' not in session:
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    current_user = User.query.filter_by(username=session['username']).first()
    
    if not current_user or not current_user.isadmin:
        flash('You do not have admin permission', 'danger')
        return redirect(url_for('home'))
    
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    if 'username' not in session:
        flash('You need to be logged in to add items to the cart', 'danger')
        return redirect(url_for('login'))
    
    quantity = int(request.form.get('quantity', 1))
    current_user = User.query.filter_by(username=session['username']).first()
    item = Item.query.get_or_404(item_id)

    cart_item = CartItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, item_id=item_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    flash('Item added to cart!', 'success')
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    if 'username' not in session:
        flash('You need to be logged in to view the cart.', 'danger')
        return redirect(url_for('login'))
    
    current_user = User.query.filter_by(username=session['username']).first()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    total_cost = sum(item.item.price * item.quantity for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_cost=total_cost)

@app.route('/update_cart/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    if 'username' not in session:
        flash('You need to be logged in to update the cart.', 'danger')
        return redirect(url_for('login'))
    
    quantity = int(request.form.get('quantity', 1))
    current_user = User.query.filter_by(username=session['username']).first()
    cart_item = CartItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()

    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
        flash('Cart updated!', 'success')
    else:
        flash('Item not found in cart', 'danger')

    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'username' not in session:
        flash('You need to be logged in to remove items from the cart', 'danger')
        return redirect(url_for('login'))
    
    current_user = User.query.filter_by(username=session['username']).first()
    cart_item = CartItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed successfully', 'successs')
    else:
        flash('Item not found in the cart', 'danger')

    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def  checkout():
    if 'username' not in session:
        flash('You need to be logged in to access this page', 'danger')
        return redirect(url_for('login'))
    
    username = session['username']
    cart_items = db.session.execute(
        text('''
            SELECT ci.quantity, i.item_name, i.price, i.item_description 
            FROM cart_item ci 
            JOIN item i ON ci.item_id = i.id 
            WHERE ci.user_id = (SELECT id FROM user WHERE username = :username)
        '''), 
        {'username': username}
    ).fetchall()

    if not cart_items:
        return render_template('cart.html', alert_message='Your cart is empty. Please add items to your cart before checking out.')

    total_cost = sum(item[2] * item[0] for item in cart_items)

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        address = request.form['address']
        payment_method = request.form['payment_method']

        result = db.session.execute(
            text('''
                INSERT INTO orders (username, name, surname, email, address, payment_method, total_cost)
                VALUES (:username, :name, :surname, :email, :address, :payment_method, :total_cost)
            '''), 
            {
                'username': username,
                'name': name,
                'surname': surname,
                'email': email,
                'address': address,
                'payment_method': payment_method,
                'total_cost': total_cost
            }
        )

        order_id = result.lastrowid

        for item in cart_items:
            order_item_insert = text('''
                INSERT INTO order_items (order_id, item_name, quantity)
                VALUES (:order_id, :item_name, :quantity)
            ''')
            db.session.execute(order_item_insert, {
                'order_id': order_id,
                'item_name': item[1],
                'quantity': item[0]
            })
        db.session.commit()

        db.session.execute(
            text('DELETE FROM cart_item WHERE user_id = (SELECT id FROM user WHERE username = :username)'),
            {'username': username}
        )
        db.session.commit()
        return redirect(url_for('order_complete', order_id=order_id))
    
    return render_template('checkout.html', cart_items=cart_items, total_cost=total_cost)

@app.route('/order_complete/<int:order_id>')
def order_complete(order_id):
    order = db.session.execute(text('SELECT * FROM orders WHERE order_id = :order_id'), {'order_id':order_id}).fetchone()
    order_items = db.session.execute(text('SELECT * FROM order_items WHERE order_id = :order_id'), {'order_id': order_id}).fetchall()

    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('home'))
    
    return render_template('order_complete.html', order=order, order_items=order_items)

@app.route('/admin/orders', methods=['GET'])
def orders():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    per_page = 10

    query = text('''
        SELECT * FROM orders
        WHERE username LIKE :search
        OR name LIKE :search
        OR surname LIKE :search
        OR email LIKE :search
        OR address LIKE :search
        ORDER BY order_id DESC
        LIMIT :limit OFFSET :offset
    ''')

    search_term = f'%{search}%'
    orders_result = db.session.execute(query, {
        'search': search_term,
        'limit': per_page,
        'offset': (page - 1) * per_page
    })

    orders = [dict(order) for order in orders_result.mappings()]

    count_query = text('''
        SELECT COUNT(*) FROM orders
        WHERE username LIKE :search
        OR name LIKE :search
        OR surname LIKE :search
        OR email LIKE :search
        OR address LIKE :search
    ''')

    total_orders = db.session.execute(count_query, {'search': search_term}).scalar()

    return jsonify({
        'orders': orders,
        'total': total_orders,
        'pages': (total_orders + per_page - 1) // per_page,
        'current_page': page
    })

@app.route('/admin/orders_page')
def orders_page():
    return render_template('orders.html')

@app.route('/admin/orders/<int:order_id>')
def order_details(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        abort(404)

    order_items = OrderItem.query.filter_by(order_id=order_id).all()

    return render_template('order_details.html', order=order, order_items=order_items)


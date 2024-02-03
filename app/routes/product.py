from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Role, Product
from app.forms import LoginForm, RegistrationForm

product = Blueprint('product', __name__)


@product.route('/products')
@login_required
def products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('products.html', products=products.items, pagination=products)


@product.route('/add-product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    manufacturer = request.form['manufacturer']

    new_product = Product(name=name, price=price, quantity=quantity, manufacturer=manufacturer)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"success": True, "message": "Product added successfully"})


@product.route('/delete-product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product has been deleted.'}), 200
    else:
        return jsonify({'error': 'Product not found'}), 404


@product.route('/update-product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if product:
        product.name = request.form['name']
        product.price = request.form['price']
        product.quantity = request.form['quantity']
        product.manufacturer = request.form['manufacturer']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Product has been updated.'}), 200
    else:
        return jsonify({'error': 'Product not found'}), 404

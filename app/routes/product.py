from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models import Product

product = Blueprint('product', __name__)


@product.route('/products')
@login_required
def products():
    page = request.args.get('page', 1, type=int)
    all_products = Product.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('products.html', products=all_products.items, pagination=all_products)


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
    found_product = Product.query.get(product_id)
    if found_product:
        db.session.delete(found_product)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product has been deleted.'}), 200
    else:
        return jsonify({'error': 'Product not found'}), 404


@product.route('/update-product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    found_product = Product.query.get(product_id)
    if found_product:
        found_product.name = request.form['name']
        found_product.price = request.form['price']
        found_product.quantity = request.form['quantity']
        found_product.manufacturer = request.form['manufacturer']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Product has been updated.'}), 200
    else:
        return jsonify({'error': 'Product not found'}), 404

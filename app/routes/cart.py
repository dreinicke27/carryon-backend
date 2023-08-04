from flask import Blueprint, request, redirect, jsonify, abort, make_response
import stripe
from app import db
from app.models.cart import Cart
from app.models.product import Product
from flask_cors import cross_origin

cartBP = Blueprint("cart", __name__, url_prefix="")

@cartBP.route("/create-checkout-session", methods=['POST'])
@cross_origin(origin="*",headers=['Content- Type', 'Authorization'])
def create_checkout_session():
    request_body = request.get_json()
    products = request_body["products"]
    items = []
    for product in products:
        line_item = {}
        line_item["quantity"] = 1
        if product["price"] == 165:
            line_item["price"] = 'price_1NYBhpFzSGyLRwvaltRdFK2s'
        else:
            line_item["price"] = 'price_1NW1ZDFzSGyLRwva7FVQsUs5'
        items.append(line_item)

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            success_url='https://carryon.onrender.com/#/success', 
            cancel_url='https://carryon.onrender.com/#/cancel',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    #return redirect(checkout_session.url, code=303)
    return jsonify(checkout_session.url), 200

@cartBP.route("/cart", methods=["POST"])
def create_cart():
    request_body = request.get_json()

    new_cart = Cart.from_dict(request_body)
    db.session.add(new_cart)
    db.session.commit()

    return {new_cart.to_dict()}, 201

@cartBP.route("/cart", methods=["GET"])
def get_all_carts():

    carts = Cart.query.all()

    cart_response = []

    for cart in carts:
        cart_response.append(cart.to_dict())

    return jsonify(cart_response), 200

@cartBP.route("/cart/<id>", methods=["GET"])
def get_cart(id):
    cart = validate_item(Cart, id)
    
    return jsonify(cart.to_dict()), 200

@cartBP.route("/cart/ip", methods=["GET"])
def get_cart_by_ip():
    try:
        ip = request.args.get('ip')

        carts = Cart.query.filter_by(ip=ip).filter_by(completed=False).all()
        cart = carts[0]

        return jsonify(cart.to_dict()), 200
    
    except Exception as e:
        return {"msg": str(e)}, 200


@cartBP.route("/cart/<id>/add", methods=["PATCH"])
def add_to_cart(id):
    cart = validate_item(Cart, id)
    request_body = request.get_json()

    product = Product.from_dict(request_body)
    product.cart = cart

    db.session.add(product)
    db.session.commit()

    return jsonify({"msg": f"Created product {product.id} and added to cart {cart.id}"}), 201


@cartBP.route("/cart/<id>/remove", methods=["PATCH"])
def remove_product_from_cart(id):
    cart = validate_item(Cart, id)

    request_body = request.get_json()
    prod_id = request_body["id"]
    product = Product.query.get(prod_id)

    cart.products.remove(product)
    Product.query.filter_by(id=prod_id).delete()
        
    db.session.commit()

    return jsonify({"msg": f"Removed product {prod_id} from cart {cart.id}"}), 201

@cartBP.route("/cart/<id>/toggle", methods=["PATCH"])
def toggle_cart_complete(id):
    cart = validate_item(Cart, id)

    cart.completed = True
        
    db.session.commit()

    return jsonify({"msg": f"Cart {cart.id} completed checkout"}), 201

@cartBP.route("/cart/<id>", methods=["DELETE"])
def delete_cart(id):
    cart = validate_item(Cart, id)

    db.session.delete(cart)
    db.session.commit()

    return {"msg": f"Cart {id} successfully deleted"}, 200


def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    return model.query.get_or_404(item_id)


from flask import Blueprint, request, redirect, jsonify, abort, make_response
import stripe
from app import db
from app.models.cart import Cart
from app.models.product import Product

cartBP = Blueprint("cart", __name__, url_prefix="")

@cartBP.route("/create-checkout-session", methods=['POST'])
def create_checkout_session():
    # if price == 165, price_key = the one here, else, the other one
    # for loop for each item in line item data, return {
    #    'price': 'price_1NW1ZDFzSGyLRwva7FVQsUs5',
    #               'quantity': 1,
    # }

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NYBhpFzSGyLRwvaltRdFK2s',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:3000/success',
            cancel_url='http://localhost:3000/cancel',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@cartBP.route("/cart", methods=["POST"])
def create_cart():
    request_body = request.get_json()

    new_cart = Cart.from_dict(request_body)
    db.session.add(new_cart)
    db.session.commit()

    return {"id": new_cart.id}, 201

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


# UPDATE patch back to like before (restaurant example) where it creates a new product and adds it 
@cartBP.route("/cart/<id>/add", methods=["PATCH"])
def add_to_cart(id):
    cart = validate_item(Cart, id)
    request_body = request.get_json()
    # prod_id = request_body["product"]["id"]
    # product = Product.query.get(prod_id)

    # cart.products.append(product)
    # db.session.commit()

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


def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    return model.query.get_or_404(item_id)


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
    #    'price': 'price_1NYBhpFzSGyLRwvaltRdFK2s',
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
    # check if IP is already in with completed == False on front end, 
    # and decide which call to make (get or post)

    new_cart = Cart.from_dict(request_body)
    db.session.add(new_cart)
    db.session.commit()

    return {"id": new_cart.id}, 201
  

@cartBP.route("/cart/<id>", methods=["GET"])
def get_cart(id):
    cart = validate_item(Cart, cart)
    
    return cart.to_dict(), 200

@cartBP.route("/cart/<id>", methods=["PUT"])
def add_to_cart(id):
#    product id from front end 
    cart = validate_item(Cart, id)
    request_body = request.get_json()
    # check if IP is already in with completed == False on front end, 
    # and decide which call to make (get or post)
    product = request_body["product"]

    cart.products.append(product)
    db.session.add(cart)
    db.session.commit()

    return jsonify({"msg": f"Added product {product.id} to cart {cart.id}"}), 201


@cartBP.route("/cart/<id>", methods=["DELETE"])
def remove_product_from_cart(id):
    cart = validate_item(Cart, id)

    request_body = request.get_json()
    product = request_body["product"]

    # get product from query 
    # Cart.query.filter(Cart.products.id == product.id).delete()

    # db.session.commit()

    return jsonify({"msg": f"Removed product {product.id} from cart {cart.id}"}), 201


def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    return model.query.get_or_404(item_id)


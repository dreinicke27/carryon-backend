from flask import Blueprint, request, redirect, jsonify
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

# @cartBP.route("/cart", methods=["POST"])
# def create_cart():
#   create cart with ip from front end 

# @cartBP.route("/cart/<id>", methods=["GET"])
# def get_cart(id):
#   check if cart with that ip address exists with complete=false, if yes, get it 
#   otherwise, create cart via post request 

# @cartBP.route("/cart/<id>", methods=["DELETE"])
# def remove_from_cart(id, attributes):
#   product id from front end

# @cartBP.route("/cart/<id>", methods=["PUT"])
# def add_to_cart(id):
#    product id from front end 


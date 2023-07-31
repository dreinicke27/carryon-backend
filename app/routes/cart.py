from flask import Blueprint, request, redirect, jsonify
import stripe
import boto3

cartBP = Blueprint("cart", __name__, url_prefix="")

@cartBP.route("/create-checkout-session", methods=['POST'])
def create_checkout_session():
    data = request.json
    # #try to get line items from request rather than here...have to be in the body from the form 
    line_item_data = data['line_items']
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
            success_url='https://carryon.onrender.com/success',
            cancel_url='https://carryon.onrender.com/cancel',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

# @cartBP.route("/")
# def root():
#     dynamodb.create_table_cart()
#     return 'Table created'

# @cartBP.route("/cart/<id>", methods=["POST"])
# def create_cart():
#     data = request.get_json()
#     response = dynamodb.write_to_cart_table(data['id'], data['products'])    
#     if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
#         return {
#             'msg': 'Added successfully',
#         }
#     return {  
#         'msg': 'Some error occcured',
#         'response': response
#     }

# @cartBP.route("/cart/<id>", methods=["GET"])
# def get_cart(id):

# @cartBP.route("/cart/<id>", methods=["DELETE"])
# def remove_from_cart(id, attributes):

# @cartBP.route("/cart/<id>", methods=["POST"])
# def add_to_cart(id):


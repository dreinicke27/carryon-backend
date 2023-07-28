#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request, jsonify
import stripe
from dotenv import load_dotenv


load_dotenv()

stripe.api_key = os.environ.get('STRIPE_SECRET_TEST_KEY')

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/config')
def config():
    return jsonify({'publishableKey':os.environ.get('STRIPE_PUBLISHABLE_TEST_KEY')})

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.json
    #try to get line items from request rather than here...have to be in the body from the form 
    line_item_data = data['line_items']
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
            success_url='https://carryon.onrender.com/',
            cancel_url='https://carryon.onrender.com/cart',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242)
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

def create_app():   

    stripe.api_key = os.environ.get('STRIPE_SECRET_TEST_KEY')

    app = Flask(__name__,
            static_url_path='',
            static_folder='public')

    if __name__ == '__main__':
        app.run(port=4242)

    #YOUR_DOMAIN = 'http://localhost:4242'

    from .routes.checkout import checkoutBP
    app.register_blueprint(checkoutBP)

    return app







import os
from flask import Flask
import stripe
from dotenv import load_dotenv


load_dotenv()

def create_app():   

    stripe.api_key = os.environ.get('STRIPE_TEST_SECRET_KEY')

    app = Flask(__name__,
            static_url_path='',
            static_folder='public')

    if __name__ == '__main__':
         app.run(port=4242)

    from .routes.cart import cartBP
    app.register_blueprint(cartBP)

    return app







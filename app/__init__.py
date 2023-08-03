import os
from flask import Flask
import stripe
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate 


load_dotenv()
db = SQLAlchemy()
migrate = Migrate()

def create_app():   

    stripe.api_key = os.environ.get('STRIPE_TEST_SECRET_KEY')

    app = Flask(__name__,
            static_url_path='',
            static_folder='public')
    
    CORS(app)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)
    
    if __name__ == '__main__':
         app.run(port=4242)

    from .routes.cart import cartBP
    app.register_blueprint(cartBP)

    from .routes.product import productBP
    app.register_blueprint(productBP)

    return app







from app import db
from app.models.cart import Cart
from app.models.product import Product

cartProducts = db.Table('cartProducts',
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)
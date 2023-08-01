from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=True)
    cart = db.relationship("Cart", back_populates="products")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
        }
    
    @classmethod
    def from_dict(cls, product_data):
        return cls(
            name = product_data["name"],
            price = product_data["price"],
        )
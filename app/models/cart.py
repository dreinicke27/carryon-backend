from app import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ip = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False)
    products = db.relationship("Product", back_populates="cart", lazy=True)

    def to_dict(self):
        products = [product.to_dict() for product in self.products]
        return {
            "id": self.id,
            "ip": self.ip,
            "completed": self.completed,
            "products": self.products
        }
    
    @classmethod
    def from_dict(cls, cart_data):
        if "completed" in cart_data.keys():
            return cls(
                ip = cart_data["ip"],
                completed = cart_data["completed"],
            )
        else:
            return cls(
                ip = cart_data["ip"],
            )
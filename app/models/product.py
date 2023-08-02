from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    price = db.Column(db.Integer)
    size = db.Column(db.String)
    collar = db.Column(db.String)
    closure = db.Column(db.String) 
    pockets = db.Column(db.String)
    length = db.Column(db.String) 
    bpocket = db.Column(db.Boolean)
    fabric = db.Column(db.String) 
    notes = db.Column(db.String) 
    price = db.Column(db.Integer)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=True)
    cart = db.relationship("Cart", back_populates="products")

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "size": self.size,
            "collar": self.collar, 
            "closure": self.closure, 
            "pockets": self.pockets, 
            "length": self.length, 
            "bpocket": self.bpocket, 
            "fabric": self.fabric, 
            "notes": self.notes, 
        }
    
    @classmethod
    def from_dict(cls, product_data):
        return cls(
            price = product_data["price"],
            size = product_data["size"],
            collar = product_data["collar"],
            closure = product_data["closure"],
            pockets = product_data["pockets"],
            length = product_data["length"],
            bpocket = product_data["bpocket"],
            fabric = product_data["fabric"],
            notes = product_data["notes"],
        )
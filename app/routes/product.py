from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.product import Product

productBP = Blueprint("product", __name__, url_prefix="/product")

@productBP.route("", methods=["POST"])
def create_product():
    request_body = request.get_json()
    new_product = Product.from_dict(request_body)

    db.session.add(new_product)
    db.session.commit()

    return {"id": new_product.id}, 201

@productBP.route("", methods=["GET"])
def get_all_products():
    response = []

    all_products = Product.query.all()
    
    for product in all_products:
        response.append(product.to_dict())

    return jsonify(response), 200

@productBP.route("/<prod_id>", methods=["PUT"])
def update_product(prod_id):
    product = validate_item(Product, prod_id)

    request_data = request.get_json()

    product.name = request_data["name"]
    product.price = request_data["price"]

    db.session.commit()

    return {"msg": f"product {prod_id} successfully updated"}, 200


@productBP.route("/<prod_id>", methods=["DELETE"])
def delete_product(prod_id):
    product = validate_item(Product, prod_id)

    db.session.delete(product)
    db.session.commit()

    return {"msg": f"product {prod_id} successfully deleted"}, 200

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    return model.query.get_or_404(item_id)
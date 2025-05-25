from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models import Customer
from . import customers_bp
from .schemas import customer_schema, customers_schema

# Create a new Customer (POST /customers)
@customers_bp.route('/', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        customer = customer_schema.load(data)
        db.session.add(customer)
        db.session.commit()
        return customer_schema.jsonify(customer), 201
    except ValidationError as ve:
        return jsonify({"validation_error": ve.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Get all Customers (GET /customers)
@customers_bp.route('/', methods=['GET'])
def get_customers():
    try:
        customers = Customer.query.all()
        return customers_schema.jsonify(customers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get a single Customer by ID (GET /customers/<id>)
@customers_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found"}), 404

# Update a Customer (PUT /customers/<id>)
@customers_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        data = request.get_json()
        updated_customer = customer_schema.load(data, instance=customer, partial=True)
        db.session.commit()
        return customer_schema.jsonify(updated_customer), 200
    except ValidationError as ve:
        return jsonify({"validation_error": ve.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Delete a Customer (DELETE /customers/<id>)
@customers_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"}), 200

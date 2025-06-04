from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from functools import wraps
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import db, limiter, cache
from app import db
from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import CustomerSchema, CustomerLoginSchema
from app.utils.util import encode_token, token_required

schema = CustomerSchema()
schema_many = CustomerSchema(many=True)
login_schema = CustomerLoginSchema()


# Create a new customer
@customers_bp.route('/', methods=['POST'])
@limiter.limit("10 per hour")
def create_customer():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        password=hashed_password
    )
    db.session.add(customer)
    db.session.commit()
    return schema.jsonify(customer), 201



# Login Route – Token Authentication
@customers_bp.route("/login", methods=["POST"])
def login_customer():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer = db.session.scalar(select(Customer).where(Customer.email == email))

    if customer and customer.password == password:
        token = encode_token(customer.id)
        return jsonify({
            "status": "success",
            "message": "Successfully logged in",
            "token": token,
        }), 200
    return jsonify({"message": "Invalid email or password"}), 401


# Authenticated route: Get tickets for logged-in customer
@customers_bp.route('/tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    try:
        tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
        return tickets_schema.jsonify(tickets), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# Get paginated customers list (with caching)
@customers_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_customers():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        pagination = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
        return customers_schema.jsonify(pagination.items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Get all customers (without pagination)
@customers_bp.route('/', methods=['GET'])
def get_customers():
    return schema_many.jsonify(Customer.query.all()), 200


# Get a single customer by ID
@customers_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found"}), 404


# Update a customer (must be authenticated)
@customers_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"message": "Unauthorized"}), 403

    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)

    try:
        db.session.commit()
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# Delete a customer
@customers_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"}), 200

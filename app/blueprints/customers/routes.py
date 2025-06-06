from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import db, ma, jwt, limiter, cache
from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema, customer_login_schema
from app.utils.util import encode_token, token_required
from app.models import Customer



# Create a new customer
@customers_bp.route('/', methods=['POST'])
@limiter.limit("10 per hour")
def create_customer():
    data = request.get_json()
    try:

        hashed_password = generate_password_hash(data['password'])
        customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=hashed_password
        )
        db.session.add(customer)
        db.session.commit()
        return customer_schema.jsonify(customer), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



# Login Route –  Authenticate customer and issues a JWT 
@customers_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    customer = Customer.query.filter_by(email=email).first()

    if not customer or not check_password_hash(customer.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    access_token = create_access_token(identity=customer.id)
        
    return jsonify({
            "status": "success",
            "message": "Successfully logged in",
            "token": access_token,
        }), 200
    
    


# READ - Get paginated customers list (with caching)
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

    if 'password' in data:
        customer.password = generate_password_hash(data['password'])

    db.session.commit()
    return customer_schema.jsonify(customer), 200



# Delete a customer (authenticated)
@customers_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    current_user_id = get_jwt_identity()
    if current_user_id != id:
        return jsonify({"error": "Unauthorized to delete this account"}), 403
    
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} deleted successfully"}), 200

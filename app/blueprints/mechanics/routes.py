from flask import request, jsonify
from app.extensions import db, ma, jwt, limiter, cache
from app.models import Mechanic
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema

# Create a new mechanic
@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    mechanic = Mechanic(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        address=data.get('address'),
        salary=data.get('salary')
    )
    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201

# Get all mechanics (with nested tickets)
@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    all_mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(all_mechanics)

# Get a single mechanic by ID (with nested tickets)
@mechanics_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    return mechanic_schema.jsonify(mechanic)

# Update a mechanic
@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json()
    mechanic.name = data.get('name', mechanic.name)
    mechanic.email = data.get('email', mechanic.email)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic)

# Delete a mechanic
@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted successfully"})

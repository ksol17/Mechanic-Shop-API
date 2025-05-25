from flask import request, jsonify
from app.extensions import db
from app.models import Mechanic
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema

# Create a new mechanic
@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    try:
        new_mechanic = mechanic_schema.load(data)
        db.session.add(new_mechanic)
        db.session.commit()
        return mechanic_schema.jsonify(new_mechanic), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

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
    for field in ['name', 'email', 'phone', 'salary']:
        setattr(mechanic, field, data.get(field, getattr(mechanic, field)))
    db.session.commit()
    return mechanic_schema.jsonify(mechanic)

# Delete a mechanic
@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted successfully"})

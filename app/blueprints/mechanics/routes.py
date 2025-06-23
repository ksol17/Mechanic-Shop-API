from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Mechanic
from app.blueprints.mechanics import mechanics_bp

# Create a new mechanic
@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    required_fields = ['name', 'email']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    mechanic = Mechanic(
        name=data['name'],
        email=data['email']
    )
    db.session.add(mechanic)
    db.session.commit()
    return jsonify({
        "id": mechanic.id,
        "name": mechanic.name,
        "email": mechanic.email
    }), 201

# Get all mechanics
@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    mechanics = Mechanic.query.all()
    return jsonify([
        {
            "id": m.id,
            "name": m.name,
            "email": m.email
        } for m in mechanics
    ]), 200

# Get a single mechanic by ID
@mechanics_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    mechanic = Mechanic.query.get(id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    return jsonify({
        "id": mechanic.id,
        "name": mechanic.name,
        "email": mechanic.email
    }), 200

# Update a mechanic
@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = Mechanic.query.get(id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    data = request.get_json()
    mechanic.name = data.get('name', mechanic.name)
    mechanic.email = data.get('email', mechanic.email)
    db.session.commit()
    return jsonify({
        "id": mechanic.id,
        "name": mechanic.name,
        "email": mechanic.email
    }), 200

# Delete a mechanic
@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = Mechanic.query.get(id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted successfully"}), 200



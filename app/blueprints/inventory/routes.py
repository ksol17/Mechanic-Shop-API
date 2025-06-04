from flask import request, jsonify
from app.extensions import db
from app.models import Inventory
from app.blueprints.inventory import inventory_bp
from app.blueprints.inventory.schemas import (
    inventory_schema, inventories_schema,
    
)
from marshmallow import ValidationError

# ------------------ INVENTORY ------------------

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    items = Inventory.query.all()
    return inventories_schema.jsonify(items), 200


@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory_item(id):
    item = Inventory.query.get(id)
    if item:
        return inventory_schema.jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404



# Create a new Inventory Part
@inventory_bp.route('/', methods=['POST'])
def create_inventory_part():
    try:
        # Validate and deserialize input
        data = request.get_json()
        new_part = inventory_schema.load(data)

        db.session.add(new_part)
        db.session.commit()

        return inventory_schema.jsonify(new_part), 201

    except ValidationError as err:
        return jsonify({"validation_errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory(id):
    item = Inventory.query.get(id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)

    db.session.commit()
    return inventory_schema.jsonify(item), 200


@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    item = Inventory.query.get(id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200

# ------------------ PART DESCRIPTIONS ------------------

@inventory_bp.route('/parts', methods=['GET'])
def get_parts():
    parts = PartDescription.query.all()
    return part_descriptions_schema.jsonify(parts), 200


@inventory_bp.route('/parts/<int:id>', methods=['GET'])
def get_part(id):
    part = PartDescription.query.get(id)
    if part:
        return part_description_schema.jsonify(part), 200
    return jsonify({"error": "Part not found"}), 404



# ------------------ SERIALIZED PARTS ------------------

@inventory_bp.route('/serialized', methods=['GET'])
def get_serialized_parts():
    parts = SerializedPart.query.all()
    return serialized_parts_schema.jsonify(parts), 200


@inventory_bp.route('/serialized/<int:id>', methods=['GET'])
def get_serialized_part(id):
    part = SerializedPart.query.get(id)
    if part:
        return serialized_part_schema.jsonify(part), 200
    return jsonify({"error": "Serialized part not found"}), 404


@inventory_bp.route('/serialized', methods=['POST'])
def create_serialized_part():
    try:
        part = serialized_part_schema.load(request.get_json())
        db.session.add(part)
        db.session.commit()
        return serialized_part_schema.jsonify(part), 201
    except ValidationError as e:
        return jsonify(e.messages), 400

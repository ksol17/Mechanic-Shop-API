from flask import request, jsonify
from app.models import Inventory
from app.extensions import db, ma, jwt, limiter, cache
from app.blueprints.inventory import inventory_bp
from app.blueprints.inventory.schemas import inventory_schema, inventories_schema


# Create a new inventory item
@inventory_bp.route('/', methods=['POST'])
def create_inventory_item():
    data = request.get_json()
    item = Inventory(
        item_name = data['item_name'],
        quantity = data['quantity'],
        price = data['price'],
        description = data.get('description', '')
    )
    db.session.add(item)
    db.session.commit()
    return inventory_schema.jsonify(item), 201

# Get all inventory items
@inventory_bp.route('/', methods=['GET'])
def get_inventory_items():
    all_items = Inventory.query.all()
    return inventories_schema.jsonify(all_items)

# Get a single inventory item by ID
@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory_item(id):
    item = Inventory.query.get_or_404(id)
    return inventory_schema.jsonify(item)

# Update an inventory item
@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory_item(id):
    item = Inventory.query.get_or_404(id)
    data = request.get_json()
    item.item_name = data.get('item_name', item.item_name)
    item.quantity = data.get('quantity', item.quantity)
    item.price = data.get('price', item.price)
    item.description = data.get('description', item.description)
    
    db.session.commit()
    return inventory_schema.jsonify(item)

# Delete an inventory item
@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory_item(id):
    item = Inventory.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"Inventory item {id} deleted successfully"}), 200


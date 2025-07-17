from app.extensions import db, ma, jwt, limiter, cache
from app.models import Inventory
from marshmallow import Schema, fields



# Inventory schema
class InventorySchema(Schema):
    id = fields.Int(dump_only=True)
    item_name = fields.Str(required=True)
    quantity = fields.Int(required=True)
    price = fields.Float(required=True)

# Schema instances
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)


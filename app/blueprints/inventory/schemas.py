from app import ma
from app.extensions import db, ma, jwt, limiter, cache
from app.models import Inventory
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema



# Inventory schema
class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True

   

# Schema instances
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)


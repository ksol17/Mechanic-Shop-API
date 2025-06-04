from app.extensions import ma
from app.models import Inventory, SerializedPart, PartDescription
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

# PartDescription schema
class PartDescriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PartDescription
        load_instance = True
        include_fk = True

    serialized_parts = fields.Nested("SerializedPartSchema", many=True, dump_only=True)

# SerializedPart schema
class SerializedPartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SerializedPart
        load_instance = True
        include_fk = True

    description = fields.Nested(PartDescriptionSchema, dump_only=True)

# Inventory schema
class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True

    tickets = fields.List(fields.String(), dump_only=True)  # Placeholder for nested ticket relationship


# Schema instances
part_description_schema = PartDescriptionSchema()
part_descriptions_schema = PartDescriptionSchema(many=True)

serialized_part_schema = SerializedPartSchema()
serialized_parts_schema = SerializedPartSchema(many=True)

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)


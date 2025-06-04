from app.extensions import ma
from app.models import ServiceTicket, Mechanic
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields


class MechanicSummarySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        fields = ("id", "name", "email")
        load_instance = True

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True
        include_relationships = True

    mechanics = fields.Nested("MechanicSchema", many=True, dump_only=True)
    customer = fields.Nested("CustomerSchema", dump_only=True)
    parts = fields.Nested("InventorySchema", many=True, dump_only=True)
    serialized_parts = fields.Nested("SerializedPartSchema", many=True, dump_only=True)

# Schema instances
ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)

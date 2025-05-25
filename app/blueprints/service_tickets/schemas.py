from app.extensions import ma
from app.models import ServiceTicket, Mechanic
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

# Nested mechanic summary for showing inside tickets
class MechanicSummarySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        fields = ("id", "name", "email")
        load_instance = True

# Main ticket schema with nested mechanics
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True
        include_relationships = True
    # Nested mechanics
    mechanics = fields.Nested(MechanicSummarySchema, many=True, dump_only=True)
    # Prevent Marshmallow from trying to deserialize the full Customer object
    customer = fields.Nested("CustomerSchema", dump_only=True)
   
# Schema instances

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)

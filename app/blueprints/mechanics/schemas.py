from app.extensions import ma
from app.models import Mechanic, MechanicServiceTicket
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True
        include_relationships = True

    mechanic_tickets = fields.Nested("MechanicServiceTicketSchema", many=True, dump_only=True)

class MechanicServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MechanicServiceTicket
        load_instance = True
        include_fk = True
        include_relationships = True

    ticket = fields.Nested("ServiceTicketSchema", dump_only=True)  # Use string reference to avoid circular import

# Schema instances
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

mechanic_ticket_schema = MechanicServiceTicketSchema()
mechanic_tickets_schema = MechanicServiceTicketSchema(many=True)

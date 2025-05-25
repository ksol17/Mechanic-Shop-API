from app.extensions import ma
from app.models import Mechanic, ServiceTicket
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

# Nested schema for ServiceTicket (minimal fields shown; you can expand as needed)
class ServiceTicketSummarySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        fields = ("id", "VIN", "service_date", "service_desc")
        load_instance = True

# Main Mechanic schema with nested tickets
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_relationships = True

    # Include related tickets
    tickets = fields.Nested(ServiceTicketSummarySchema, many=True)

# Schema instances
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

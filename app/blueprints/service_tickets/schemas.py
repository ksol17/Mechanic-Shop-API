from app.extensions import ma, jwt, limiter, cache
from app.models import ServiceTicket
from marshmallow import Schema, fields



class MechanicSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    
class CustomerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(load_only=True)

class ServiceTicketSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)
    customer_id = fields.Int(required=True)
    customer = fields.Nested(CustomerSchema, dump_only=True)
    mechanics = fields.List(fields.Nested(MechanicSchema), dump_only=True)

# Schema instances
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

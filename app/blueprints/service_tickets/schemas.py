from app.extensions import db, ma, jwt, limiter, cache
from app.models import ServiceTicket, Mechanic
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields



class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True
       

# Schema instances
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

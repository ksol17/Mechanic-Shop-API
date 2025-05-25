from app.extensions import ma
from app.models import Customer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True


        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True) 


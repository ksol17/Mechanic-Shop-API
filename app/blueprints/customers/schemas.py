from app.models import Customer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE
from app.extensions import ma

# Schema for Customer model
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True
        
    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    phone = ma.auto_field(required=True)
    password = ma.auto_field(required=True)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Schema for login validation (only email and password)
class CustomerLoginSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer

    email = ma.auto_field()
    password = ma.auto_field()

customer_login_schema = CustomerLoginSchema()

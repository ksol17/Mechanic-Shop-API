from app.models import Customer
from marshmallow import Schema, fields
from app.extensions import ma

# Schema for Customer model
class CustomerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(load_only=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Schema for login validation (only email and password)
class CustomerLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)

customer_login_schema = CustomerLoginSchema()
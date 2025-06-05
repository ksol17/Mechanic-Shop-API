from app import ma
from app.models import Customer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE
from app.extensions import db, ma, jwt, limiter, cache

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True
        exclude = ("password",)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Schema for login validation (only email and password)
class CustomerLoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        fields = ("email", "password")
        load_instance = True

customer_login_schema = CustomerLoginSchema()

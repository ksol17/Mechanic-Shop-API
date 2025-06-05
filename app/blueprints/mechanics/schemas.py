from app.extensions import db, ma, jwt, limiter, cache

from app.models import Mechanic
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        

  


# Schema instances
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


from app.extensions import db, ma, jwt, limiter, cache
from marshmallow import Schema, fields

from app.models import Mechanic

class MechanicSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)

# Schema instances
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


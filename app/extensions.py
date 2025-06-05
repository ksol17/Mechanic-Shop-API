from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate




# Base class for SQLAlchemy type annotations
class Base(DeclarativeBase):
    pass

# Extensions
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
migrate = Migrate()

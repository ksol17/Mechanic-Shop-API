from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# Creating an instance of Limiter to limit the rate of requests
# This is useful for preventing abuse and ensuring fair usage of resources.
limiter = Limiter(key_func=get_remote_address)


class Base(DeclarativeBase):
    pass


ma = Marshmallow()
db = SQLAlchemy()

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})


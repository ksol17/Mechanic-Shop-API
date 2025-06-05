from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from .extensions import db, ma
from flask_jwt_extended import JWTManager
from app.models import db
from app.extensions import db, ma, jwt, limiter, cache
from config import DevelopmentConfig
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import DevelopmentConfig

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    
    #Load app configuration 
    app.config.from_object(config_class)


    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)


    # Register blueprints

    from app.blueprints.customers import customers_bp
    from app.blueprints.mechanics import mechanics_bp
    from app.blueprints.inventory import inventory_bp
    from app.blueprints.service_tickets import service_tickets_bp

 
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')

   

    return app

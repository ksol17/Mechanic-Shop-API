from flask import Flask
from .extensions import db, ma
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp
from flask_jwt_extended import JWTManager
from app.models import db
from .extensions import ma, limiter, cache

jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config['JSON_SECRET_KEY'] = "dev-secret-key"

    #Load app configuration 
    app.config.from_object(f'config.{config_name}')

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Register blueprints
 
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app

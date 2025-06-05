from flask import Flask
from config import DevelopmentConfig
from app.extensions import db, ma, jwt, limiter, cache, migrate
from app import models



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
    migrate.init_app(app, db)


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

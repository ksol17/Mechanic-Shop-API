from flask import Flask
from config import DevelopmentConfig
from app.extensions import db, ma, jwt, limiter, cache, migrate
from app import models
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs' # URL for exposing Swagger UI(without trialing '/')
API_URL = '/static/swagger.yaml' # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Mechanic Shop Management API',
    }
)                                                                                             

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
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) #Registering our swagger blueprint

   

    return app

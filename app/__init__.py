import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_caching import Cache
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
limiter = Limiter(key_func=lambda: "global")  # Example key_func; customize if needed
cache = Cache()
migrate = Migrate()

# Swagger setup
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Mechanic Shop Management API'}
)

def create_app(config_class):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Ensure database URI exists, otherwise use a fallback for local use
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "SQLALCHEMY_DATABASE_URI", "sqlite:///Mechanic_Shop.db"
        )

    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
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
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app

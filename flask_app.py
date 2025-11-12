from dotenv import load_dotenv
import os
from app import create_app, db
from config import DevelopmentConfig, ProductionConfig

# Choose env file
env_file = ".env.production" if os.getenv("FLASK_ENV") == "production" else ".env.development"
load_dotenv(env_file)

# Determine environment
env = os.getenv("FLASK_ENV", "development").lower()

# Pick config class
config = ProductionConfig if env == "production" else DevelopmentConfig

# Create Flask app
app = create_app(config)

# Initialize database tables (optional)
with app.app_context():
    db.create_all()



#gunicorn flask_app:app
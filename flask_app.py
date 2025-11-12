from dotenv import load_dotenv
import os
from app import create_app, db
from config import ProductionConfig, DevelopmentConfig


# Load .env for local development
load_dotenv()

# Pick config based on FLASK_ENV
env = os.getenv("FLASK_ENV", "development").lower()
config = ProductionConfig if env == "production" else DevelopmentConfig

# Create Flask app
app = create_app(config)

# Optional: create tables if they don’t exist
with app.app_context():
    db.create_all()

#gunicorn flask_app:app
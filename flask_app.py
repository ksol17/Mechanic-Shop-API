from dotenv import load_dotenv
import os
from app import create_app, db
from config import  DevelopmentConfig, TestingConfig, ProductionConfig


# Load environment variables from .env file
load_dotenv()

# Determine the environment
env = os.getenv('FLASK_ENV', 'development').lower()

# Pick configuration based on environment
if env == 'production':
    config = ProductionConfig
elif env == 'testing':
    config = TestingConfig
else:
    config = DevelopmentConfig

# Create Flask app using selected configuration
app = create_app(config)

# Initialize database tables if needed(Production environment should handle migrations separately)
with app.app_context():
    db.create_all()
    

#gunicorn flask_app:app
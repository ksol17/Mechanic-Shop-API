from dotenv import load_dotenv
import os
from app import create_app, db
from config import ProductionConfig, DevelopmentConfig

# Choose the correct env file
env_file = '.env.production' if os.getenv('FLASK_ENV') == 'production' else '.env.development'
load_dotenv(env_file)

# SELECT CONFIG
config = ProductionConfig if os.getenv('FLASK_ENV') == 'production' else DevelopmentConfig

# Create flask app
app = create_app(config)

# Optional: create tables if they don't exist
with app.app_context():
    db.create_all()


#gunicorn flask_app:app
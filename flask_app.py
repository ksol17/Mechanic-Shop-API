from dotenv import load_dotenv
import os
from app import create_app, db
from config import ProductionConfig

load_dotenv(".env.production")  

app = create_app(ProductionConfig)

with app.app_context():
    db.create_all()


#gunicorn flask_app:app
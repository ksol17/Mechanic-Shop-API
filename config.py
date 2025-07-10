
from dotenv import load_dotenv
load_dotenv()

import os


class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mechanic_shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'  # Use SimpleCache for development

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY= 'test'
    CACHE_TYPE = 'SimpleCache'  # Disable caching in tests
    

class ProductionConfig:
    debug = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mechanic_shop.db'
    CACHE_TYPE = 'SimpleCache'  # Use SimpleCache for production
    SECRET_KEY = os.environ.get('SECRET_KEY')
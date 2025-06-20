
from dotenv import load_dotenv
load_dotenv()

import os


class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mechanic_shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY= 'test'
    

class ProductionConfig:
    pass
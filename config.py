
from dotenv import load_dotenv
load_dotenv()

import os


class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mechanic_shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class TestingConfig:
    pass
    

class ProductionConfig:
    pass

from dotenv import load_dotenv
load_dotenv()

import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    RATELIMIT_STORAGE_URL = os.getenv("RATELIMIT_STORAGE_URL")
    
class TestingConfig:
    pass
    

class ProductionConfig:
    pass
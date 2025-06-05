import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("mysql+mysqlconnector://root:Preciosa2016!@localhost/Mechanic_Shop")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("dev-secret-key")
    RATELIMIT_STORAGE_URL = os.getenv("redis://localhost:6379")


class TestingConfig:
    pass
    

class ProductionConfig:
    pass
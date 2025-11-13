import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'sqlite:///Mechanic_Shop.db')
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'  

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URI", "sqlite:///testing.db"
    )
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI= os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = 'SimpleCache'
    SECRET_KEY= 'supersecretkey12345'

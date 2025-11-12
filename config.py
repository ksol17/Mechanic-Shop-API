import os






class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Preciosa16!@localhost/mechanic_shop_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'
    SECRET_KEY = os.getenv("SECRET_KEY")

import os






class DevelopmentConfig:
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Preciosa16!@localhost/mechanic_shop_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'  # Use SimpleCache for development

class TestingConfig:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'  # Disable caching in tests
    

class ProductionConfig:
   
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'  # Use SimpleCache for production


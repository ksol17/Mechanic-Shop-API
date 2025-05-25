class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///Mechanic_Shop.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev-secret-key"

class TestingConfig:
    pass
    

class ProductionConfig:
    pass
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///Mechanic_Shop.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev-secret-key"
    RATELIMIT_STORAGE_URL = "redis://localhost:6379"


class TestingConfig:
    pass
    

class ProductionConfig:
    pass
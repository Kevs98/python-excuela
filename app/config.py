import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you`ll never guess"
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/excuela")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

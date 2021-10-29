"""Flask aplication config."""
import os


class Config:
    """Configuration for app."""

    PORT = "5000"
    HOST = "0.0.0.0"
    DEBUG = False


class DevelopmentConfig(Config):
    """Dev config."""

    message_db_path = os.getenv("MESSAGE_DB_PATH", "/messaging")
    sqlalchemy_file = os.path.join(message_db_path, "db.sqlite")
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(sqlalchemy_file)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")

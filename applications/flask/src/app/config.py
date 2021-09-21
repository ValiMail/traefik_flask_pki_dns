"""Flask aplication config."""
import os


class Config:
    """Configuration for app."""

    PORT = "5000"
    HOST = "0.0.0.0"
    DEBUG = False


class DevelopmentConfig(Config):
    """Dev config."""

    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True

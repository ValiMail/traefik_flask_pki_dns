"""Initialize app."""
import os

from flask import Flask
import flask_login
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import DevelopmentConfig
from .config import ProductionConfig

db = SQLAlchemy()
csrf = CSRFProtect()
# migrate = Migrate()


def create_app():
    """Create the app."""
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1)
    if os.getenv("PRODUCTION_ENV"):
        app.config.from_object(ProductionConfig())
    else:
        app.config.from_object(DevelopmentConfig())
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "helloworldly")
    # db.init_app(app)
    csrf.init_app(app)
    # migrate.init_app(app, db)
    # login_manager = flask_login.LoginManager()
    # login_manager.login_view = "auth.login"
    # login_manager.init_app(app)

    # from .models import User
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app

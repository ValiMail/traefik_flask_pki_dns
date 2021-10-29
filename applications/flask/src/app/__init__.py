"""Initialize app."""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .weblib.config import DevelopmentConfig

db = SQLAlchemy()

api_hostname = "api.{}".format(os.getenv("BASE_DNS_NAME"))
portal_hostname = "portal.{}".format(os.getenv("BASE_DNS_NAME"))

def create_app():
    """Create the app."""
    app = Flask(__name__)
    conf = DevelopmentConfig
    app.config.from_object(conf())
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    db.init_app(app)

    from .entry import entry as entry_blueprint
    app.register_blueprint(entry_blueprint)

    if not os.path.exists(conf.message_db_path):
        print("Creating DB directory: {}".format(conf.message_db_path))
        os.makedirs(conf.message_db_path)
    if not os.path.isfile(conf.sqlalchemy_file):
        print(dir(conf))
        print("Creating DB {}".format(conf.SQLALCHEMY_DATABASE_URI))
        with app.app_context():
            db.create_all(app=app)
            db.session.commit()
            db.session.close()
    return app

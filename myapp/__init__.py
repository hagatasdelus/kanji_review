import os
from secrets import token_hex

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask import Flask

base_dir = os.path.abspath(os.path.dirname(__name__))
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = token_hex()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        base_dir, "data.sqlite"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    from myapp.views import bp

    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app, db)
    return app

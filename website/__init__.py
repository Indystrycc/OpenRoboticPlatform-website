from os import environ
from time import sleep

from flask import Flask, Response
from flask_login import LoginManager
from .secrets_manager import *
from flask_sqlalchemy import SQLAlchemy
from MySQLdb.constants.CR import CONNECTION_ERROR
from sqlalchemy.exc import OperationalError

from .secrets_manager import *

# DB_NAME = 'database.db'
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["RECAPTCHA_PUBLIC_KEY"] = RECAPTCHA_PUBLIC_KEY
    app.config["RECAPTCHA_PRIVATE_KEY"] = RECAPTCHA_PRIVATE_KEY
    # app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f'mysql://root:rootroot@{environ.get("DB_HOST") or "127.0.0.1"}:3306/orp_db'
    # db = SQLAlchemy(app)
    db.init_app(app)

    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from . import models

    with app.app_context():
        for _ in range(5):
            try:
                db.create_all()
                break
            except OperationalError as err:
                # db may not be running yet
                if err.orig.args[0] == CONNECTION_ERROR:
                    sleep(3)
                else:
                    raise
        db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    @app.after_request
    def set_important_headers(response: Response):
        response.headers.set("X-Content-Type-Options", "nosniff")
        return response

    return app

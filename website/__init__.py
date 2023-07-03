import uuid
from concurrent.futures import ProcessPoolExecutor
from os import getenv

from flask import Flask, Response
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from .secrets_manager import *

db = SQLAlchemy()
migrate = Migrate()
compression_process = (
    ProcessPoolExecutor(1) if getenv("FLASK_ENV") == "production" else None
)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["RECAPTCHA_PUBLIC_KEY"] = RECAPTCHA_PUBLIC_KEY
    app.config["RECAPTCHA_PRIVATE_KEY"] = RECAPTCHA_PRIVATE_KEY

    if getenv("TRUSTED_PROXIES", "0") == "1":
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f'mysql://root:rootroot@{getenv("DB_HOST", "127.0.0.1")}:3306/orp_db'
    db.init_app(app)
    migrate.init_app(app, db)

    from .auth import auth
    from .views import views
    from .views_admin import views_admin

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views_admin, url_prefix="/admin/")

    # Register models
    from . import models

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(uuid.UUID(id))

    @app.after_request
    def set_important_headers(response: Response):
        response.headers.set("X-Content-Type-Options", "nosniff")
        return response

    return app

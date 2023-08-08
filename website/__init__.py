import uuid, os
from concurrent.futures import ProcessPoolExecutor
from os import getenv

from flask import Flask, Response, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix

from .secrets_manager import *

production = getenv("FLASK_ENV") == "production"

db = SQLAlchemy()
migrate = Migrate()
talisman = Talisman()
csrf = SeaSurf()
compression_process = ProcessPoolExecutor(1) if production else None

default_csp = {
    "default-src": "'none'",
    "base-uri": "'none'",
    "form-action": "'self'",
    "style-src": ["'self'", "https://fonts.googleapis.com"],
    "font-src": "https://fonts.gstatic.com",
    "script-src": "",  # allow only nonce-based scripts (csp_nonce() adds values here)
    "connect-src": "'self'",
    "manifest-src": "'self'",
    "img-src": [
        "'self'",
        "data:",  # Bootstrap has some SVGs as data: URL in the stylesheet
    ],
}
csp_captcha = dict(
    default_csp,
    **{
        "script-src": "'strict-dynamic'",
        "frame-src": [
            "https://www.google.com/recaptcha/",
            "https://recaptcha.google.com/recaptcha/",
        ],
    },
)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["RECAPTCHA_PUBLIC_KEY"] = RECAPTCHA_PUBLIC_KEY
    app.config["RECAPTCHA_PRIVATE_KEY"] = RECAPTCHA_PRIVATE_KEY
    app.config["MAILERLITE_API_KEY"] = MAILERLITE_API_KEY
    if production:
        app.config["SERVER_NAME"] = getenv("DOMAIN", "orp.testing")

    if getenv("TRUSTED_PROXIES", "0") == "1":
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f'mysql://root:rootroot@{getenv("DB_HOST", "127.0.0.1")}:3306/orp_db'
    db.init_app(app)
    migrate.init_app(app, db)
    talisman.init_app(
        app,
        content_security_policy=default_csp,
        content_security_policy_nonce_in=["script-src"],
        force_https=production,
        permissions_policy={
            "accelerometer": (),
            "camera": (),
            "browsing-topics": (),  # prevent Chrome from tracking visitors on this website
            "geolocation": (),
            "gyroscope": (),
            "magnetometer": (),
            "microphone": (),
            "payment": (),
            "usb": (),
        },
        session_cookie_secure=production,
        strict_transport_security=False,  # nginx already does it
        referrer_policy="same-origin",
        x_xss_protection=False,  # it's not supported any more, because it wasn't always working and could introduce new vulnerabilities
    )
    app.config["CSRF_COOKIE_SECURE"] = production
    app.config["CSRF_COOKIE_HTTPONLY"] = True
    csrf.init_app(app)

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
        # enable process isolation and prevent XS-Leaks
        response.headers.set("Cross-Origin-Opener-Policy", "same-origin")
        # block no-cors cross-origin requests to our site, change it (on /static) if we want to allow cross-origin embedding of our resources
        response.headers.set("Cross-Origin-Resource-Policy", "same-origin")
        # only allow loading resources with CORP or (if marked as crossorigin) CORS
        response.headers.set("Cross-Origin-Embedder-Policy", "require-corp")
        return response

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static/assets/favicon"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    return app

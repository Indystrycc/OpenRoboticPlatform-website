import uuid
from concurrent.futures import ProcessPoolExecutor
from functools import wraps
from os import getenv, path
from typing import Any, Callable, ParamSpec, TypeVar

from flask import Flask, Response, g, request, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from werkzeug.middleware.proxy_fix import ProxyFix

from .secrets_manager import *
from .utils import extend_talisman_csp


class BaseModel(DeclarativeBase, MappedAsDataclass):
    pass


production = getenv("FLASK_ENV") == "production"
DOMAIN = getenv("DOMAIN", "orp.testing")

db = SQLAlchemy(model_class=BaseModel)
from . import models

migrate = Migrate()
talisman = Talisman()
csrf = SeaSurf()
login_manager: LoginManager = LoginManager()
compression_process = ProcessPoolExecutor(1) if production else None

default_csp: dict[str, str | list[str]] = {
    "default-src": "'none'",
    "base-uri": "'none'",
    "form-action": "'self'",
    "style-src": ["'self'", "https://fonts.googleapis.com"],
    "font-src": "https://fonts.gstatic.com",
    "script-src": "'strict-dynamic'",  # allow only nonce-based scripts (csp_nonce() adds values here) and other injected by those
    "connect-src": "'self'",
    "manifest-src": "'self'",
    "img-src": [
        "'self'",
        "data:",  # Bootstrap has some SVGs as data: URL in the stylesheet
    ],
}
if production:
    default_csp = extend_talisman_csp(
        default_csp,
        {
            "connect-src": f"https://analytics.{DOMAIN}",
            "img-src": f"https://analytics.{DOMAIN}",
        },
    )
csp_captcha = extend_talisman_csp(
    default_csp,
    {
        "frame-src": [
            "https://www.google.com/recaptcha/",
            "https://recaptcha.google.com/recaptcha/",
        ],
    },
)
csp_kickstarter_ext = {"frame-src": "https://www.kickstarter.com"}

T = TypeVar("T")
P = ParamSpec("P")


def disable_COEP(f: Callable[P, T]) -> Callable[P, T]:
    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        g.disable_COEP = True
        return f(*args, **kwargs)

    return wrapper


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["RECAPTCHA_PUBLIC_KEY"] = RECAPTCHA_PUBLIC_KEY
    app.config["RECAPTCHA_PRIVATE_KEY"] = RECAPTCHA_PRIVATE_KEY
    app.config["MAILERLITE_API_KEY"] = MAILERLITE_API_KEY
    if production:
        app.config["SERVER_NAME"] = DOMAIN
        app.jinja_env.globals["DOMAIN"] = DOMAIN
        app.jinja_env.globals["ENV_production"] = True

    if getenv("TRUSTED_PROXIES", "0") == "1":
        # This assignment is correct. See https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)  # type: ignore[method-assign]

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f'mysql://root:rootroot@{getenv("DB_HOST", "127.0.0.1")}:3306/orp_db'
    )
    db.init_app(app)
    migrate.init_app(app, db)
    talisman.init_app(
        app,
        content_security_policy=default_csp,
        content_security_policy_nonce_in=["script-src"],
        force_https=production,
        permissions_policy={
            "accelerometer": "()",
            "camera": "()",
            "browsing-topics": "()",  # prevent Chrome from tracking visitors on this website
            "geolocation": "()",
            "gyroscope": "()",
            "magnetometer": "()",
            "microphone": "()",
            "payment": "()",
            "usb": "()",
        },
        session_cookie_secure=production,
        strict_transport_security=False,  # nginx already does it
        referrer_policy="same-origin",
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

    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id: str) -> models.User | None:
        return db.session.get(models.User, uuid.UUID(id))

    @app.before_request
    def initialize_request_vars():
        g.DNT = request.headers.get("DNT", "0") == "1"

    @app.after_request
    def set_important_headers(response: Response) -> Response:
        # enable process isolation and prevent XS-Leaks
        response.headers.set("Cross-Origin-Opener-Policy", "same-origin")
        # block no-cors cross-origin requests to our site, change it (on /static) if we want to allow cross-origin embedding of our resources
        response.headers.set("Cross-Origin-Resource-Policy", "same-origin")
        # Allow disabling COEP, because Kickstarter and YouTube embeds/iframes do not have CORP header (why???) and credentialless iframes are not a thing
        if not g.get("disable_COEP", False):
            # only allow loading resources with CORP or (if marked as crossorigin) CORS
            response.headers.set("Cross-Origin-Embedder-Policy", "require-corp")
        elif production:
            # Make sure that nginx does not implicitly add the COEP header to this response
            response.headers.set("__No-Implicit-COEP", "1")
        return response

    @app.context_processor
    def inject_template_globals() -> dict[str, Any]:
        from .session_utils import get_session

        return {"user": get_session()}

    @app.route("/favicon.ico")
    def favicon() -> Response:
        return send_from_directory(
            path.join(app.root_path, "static/assets/favicon"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    return app

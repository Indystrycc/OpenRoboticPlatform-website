from time import sleep
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .secret import *
from flask_recaptcha import ReCaptcha
from sqlalchemy.exc import OperationalError

#DB_NAME = 'database.db'
db = SQLAlchemy()
recaptcha = ReCaptcha()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
    app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY
    #app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rootroot@localhost/orp_db'
    #db = SQLAlchemy(app)
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from . import models

    with app.app_context():
        for _ in range(5):
            try:
                db.create_all()
                break
            except OperationalError as err:
                # 2002 is connection error - db may not be running yet
                if err.orig.args[0] == 2002:
                    sleep(3)
                else:
                    raise
        db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    return app

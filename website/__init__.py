from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mysqldb import MySQL

#DB_NAME = 'database.db'
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yi?o^E>Id(3R!)ry,ogfVrZ5dqP#+_Q9'
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
        db.create_all()
        db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    return app

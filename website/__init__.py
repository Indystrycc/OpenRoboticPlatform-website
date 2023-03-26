from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yi?o^E>Id(3R!)ry,ogfVrZ5dqP#+_Q9'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Note

    createDatabase(app)
    return app

def createDatabase(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')
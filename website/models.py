from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(163))
    username = db.Column(db.String(20), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))
    name_github = db.Column(db.String(100))
    name_youtube = db.Column(db.String(100))
    name_instagram = db.Column(db.String(100))


class Part(db.Model):
    # instead of autoincrementing it shoud be a random 5 digit hex value
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(5000))
    image = db.Column(db.String(100), unique=True)
    # category examples: plates, wheels, other, holders & adapters for: sensors, microcontrollers & SBCs, motors, cameras
    category = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    verified = db.Column(db.Boolean, default=False)
    featured = db.Column(db.Boolean, default=False)
    public = db.Column(db.Boolean, default=False)
    rejected = db.Column(db.Boolean, default=False)
    downloads = db.Column(db.Integer, default=0)
    tags = db.Column(db.String(200))


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey("part.id"))
    file_name = db.Column(db.String(100), unique=True)

    part = db.relationship("Part", backref=db.backref("files", lazy=True))

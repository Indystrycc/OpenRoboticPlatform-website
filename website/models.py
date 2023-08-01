import uuid

from flask_login import UserMixin
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(163))
    username = db.Column(db.String(20), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))
    name_github = db.Column(db.String(100))
    name_youtube = db.Column(db.String(100))
    name_instagram = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=func.now())

    parts: Mapped[list["Part"]] = db.relationship("Part", back_populates="author")


class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(5000))
    image = db.Column(db.String(100), unique=True)
    category = db.Column(db.Integer, db.ForeignKey("category.id"))
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("user.id"))
    date = db.Column(db.DateTime, default=func.now())
    verified = db.Column(db.Boolean, default=False)
    featured = db.Column(db.Boolean, default=False)
    public = db.Column(db.Boolean, default=False)
    rejected = db.Column(db.Boolean, default=False)
    downloads = db.Column(db.Integer, default=0)
    tags = db.Column(db.String(200))
    views = db.Column(db.Integer, nullable=False, default=0)

    cat = db.relationship("Category", backref=db.backref("part", lazy=True))
    author: Mapped[User] = db.relationship("User", back_populates="parts")


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey("part.id"))
    file_name = db.Column(db.String(100), unique=True)

    part = db.relationship("Part", backref=db.backref("files", lazy=True))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    parent_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    subcategories: Mapped[list["Category"]] = db.relationship(
        "Category", back_populates="parent_cat"
    )
    parent_cat: Mapped["Category"] = db.relationship(
        "Category", back_populates="subcategories", remote_side=[id]
    )


class View(db.Model):
    view_event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=True)
    ip = db.Column(db.String(45), nullable=True)
    part_id = db.Column(db.Integer, db.ForeignKey("part.id"), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False, default=func.now())


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_users = db.Column(db.Integer)
    total_verified_users = db.Column(db.Integer)
    total_parts = db.Column(db.Integer)
    total_verified_parts = db.Column(db.Integer)
    total_featured_parts = db.Column(db.Integer)
    total_rejected_parts = db.Column(db.Integer)
    total_files = db.Column(db.Integer)
    total_views = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=func.now())

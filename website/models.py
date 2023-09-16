import enum
import os
import uuid
from dataclasses import dataclass

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
    last_modified = db.Column(db.DateTime)

    cat = db.relationship("Category", backref=db.backref("part", lazy=True))
    author: Mapped[User] = db.relationship("User", back_populates="parts")
    files: Mapped[list["File"]] = db.relationship("File", back_populates="part")

    @property
    def thumbnail(self):
        @dataclass
        class ThumbnailDetails:
            fallback: str
            """Fallback (jpg or png) thumbnail to be used in <img>"""
            optimized: list[tuple[str, str]]
            """An ordered list of (filename, mime type) tuples in preferred order"""

        base, ext = os.path.splitext(self.image)
        preferred_thumnails = [(base + ".webp", "image/webp")]
        ext = ext.lower()
        fallback_thumbnail = base + (".png" if ext == ".png" else ".jpg")
        return ThumbnailDetails(
            fallback=fallback_thumbnail, optimized=preferred_thumnails
        )


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey("part.id"))
    file_name = db.Column(db.String(100), unique=True)

    part: Mapped[Part] = db.relationship("Part", back_populates="files")


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
    user_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
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


class TokenType(enum.Enum):
    mail_confirmation = 1
    password_reset = 2


class EmailToken(db.Model):
    token = db.Column(db.BINARY(32), primary_key=True)
    token_type = db.Column(db.Enum(TokenType), nullable=False)
    user_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_on = db.Column(db.DateTime, nullable=False, default=func.now())

    user: Mapped[User] = db.relationship()

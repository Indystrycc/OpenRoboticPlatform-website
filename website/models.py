import enum
import os
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from flask_login import UserMixin
from sqlalchemy import BINARY, UUID, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from . import BaseModel, db

if TYPE_CHECKING:
    # db.Model is based on BaseModel, but the type checker doesn't see this
    # ignore is necessary because of https://github.com/python/mypy/issues/8603#issuecomment-1245490717
    class Model(db.Model, BaseModel):  # type: ignore[name-defined,misc]
        pass

else:
    Model = db.Model


class User(UserMixin, Model):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default_factory=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(163))
    username: Mapped[str] = mapped_column(String(20), unique=True)
    confirmed: Mapped[bool] = mapped_column(default=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    image: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    name_github: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    name_youtube: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    name_instagram: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    is_admin: Mapped[bool] = mapped_column(default=False)
    date: Mapped[datetime] = mapped_column(default=func.now(), init=False)

    parts: Mapped[list["Part"]] = relationship(
        "Part", back_populates="author", default_factory=list
    )


class Part(Model):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(5000))
    image: Mapped[str] = mapped_column(String(100), unique=True)
    category: Mapped[int] = mapped_column(ForeignKey("category.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id")
    )
    date: Mapped[datetime] = mapped_column(default=func.now(), init=False)
    verified: Mapped[bool] = mapped_column(default=False)
    featured: Mapped[bool] = mapped_column(default=False)
    public: Mapped[bool] = mapped_column(default=False)
    rejected: Mapped[bool] = mapped_column(default=False)
    downloads: Mapped[int] = mapped_column(default=0, init=False)
    tags: Mapped[str] = mapped_column(String(200), default_factory=str)
    views: Mapped[int] = mapped_column(default=0, init=False)
    last_modified: Mapped[Optional[datetime]] = mapped_column(default=None, init=False)

    cat: Mapped["Category"] = relationship(
        "Category", back_populates="parts", init=False
    )
    author: Mapped[User] = relationship("User", back_populates="parts", init=False)
    files: Mapped[list["File"]] = relationship(
        "File", back_populates="part", default_factory=list
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="part", cascade="all, delete-orphan", default_factory=list
    )

    @property
    def thumbnail(self) -> "ThumbnailDetails":
        base, ext = os.path.splitext(self.image)
        preferred_thumbnails: list[tuple[str, str]] = [(base + ".webp", "image/webp")]
        ext = ext.lower()
        fallback_thumbnail = base + (".png" if ext == ".png" else ".jpg")
        return ThumbnailDetails(
            fallback=fallback_thumbnail, optimized=preferred_thumbnails
        )


class File(Model):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    part_id: Mapped[int] = mapped_column(ForeignKey("part.id"))
    file_name: Mapped[str] = mapped_column(String(100), unique=True)

    part: Mapped[Part] = relationship("Part", back_populates="files", init=False)


class Category(Model):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(50))
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("category.id"), default=None
    )

    subcategories: Mapped[list["Category"]] = relationship(
        "Category", back_populates="parent_cat", default_factory=list
    )
    parent_cat: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="subcategories", remote_side=[id], init=False
    )
    parts: Mapped[list[Part]] = relationship(
        "Part", back_populates="cat", default_factory=list
    )


class View(Model):
    view_event_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    part_id: Mapped[int] = mapped_column(ForeignKey("part.id"))
    ip: Mapped[Optional[str]] = mapped_column(String(45))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        default=None,
    )
    event_date: Mapped[datetime] = mapped_column(default=func.now(), init=False)


class Stats(Model):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    total_users: Mapped[Optional[int]]
    total_verified_users: Mapped[Optional[int]]
    total_parts: Mapped[Optional[int]]
    total_verified_parts: Mapped[Optional[int]]
    total_featured_parts: Mapped[Optional[int]]
    total_rejected_parts: Mapped[Optional[int]]
    total_files: Mapped[Optional[int]]
    total_views: Mapped[Optional[int]]
    date: Mapped[datetime] = mapped_column(default=func.now())


class TokenType(enum.Enum):
    mail_confirmation = 1
    password_reset = 2


class EmailToken(Model):
    token: Mapped[bytes] = mapped_column(BINARY(32), primary_key=True)
    token_type: Mapped[TokenType] = mapped_column(Enum(TokenType))
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE")
    )
    created_on: Mapped[datetime] = mapped_column(default=func.now(), init=False)

    user: Mapped[User] = relationship(init=False)


class Comment(Model):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    content: Mapped[str] = mapped_column(String(1000))
    date: Mapped[datetime] = mapped_column(default=func.now(), init=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE")
    )
    part_id: Mapped[int] = mapped_column(ForeignKey("part.id", ondelete="CASCADE"))
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comment.id", ondelete="CASCADE"))

    author: Mapped[User] = relationship("User", init=False)
    part: Mapped[Part] = relationship("Part", init=False)
    parent: Mapped[Optional["Comment"]] = relationship("Comment", remote_side=[id], init=False)
    replies: Mapped[list["Comment"]] = relationship(
        "Comment", 
        back_populates="parent", 
        cascade="all, delete-orphan",
        default_factory=list,
        init=False
    )


@dataclass
class ThumbnailDetails:
    fallback: str
    """Fallback (jpg or png) thumbnail to be used in <img>"""
    optimized: list[tuple[str, str]]
    """An ordered list of (filename, mime type) tuples in preferred order"""

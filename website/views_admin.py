from functools import wraps

from bleach import clean
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from markupsafe import Markup
from sqlalchemy import exists, select
from sqlalchemy.orm import joinedload

from . import db
from .models import Category, Part
from .session_utils import get_user

views_admin = Blueprint("views_admin", __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_user()
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


@views_admin.before_request
@login_required
@admin_required
def before_request():
    pass


@views_admin.route("/panel")
def panel():
    parts = db.paginate(
        select(Part).options(
            joinedload(Part.author),
            joinedload(Part.cat),
            joinedload(Part.cat, Category.parent_cat),
        ),
        per_page=20,
    )
    return render_template("adminpanel.html", parts=parts)


@views_admin.route("/editpart:<int:part_number>", methods=["GET", "POST"])
def editPart(part_number: int):
    part = db.session.get(Part, part_number)
    if part is None:
        abort(404)

    if request.method == "POST":
        name = clean(request.form.get("name", part.name))
        description = clean(request.form.get("description", part.description))
        tags = clean(request.form.get("tags", part.tags))
        verified = request.form.get("verified")
        public = request.form.get("public")
        rejected = request.form.get("rejected")
        featured = request.form.get("featured")
        category = request.form.get("category", part.category, type=int)

        # Update the part with the new values using the provided part_id and updated_values
        part.name = name
        part.description = description
        part.category = category
        part.verified = True if verified == "on" else False
        part.featured = True if featured == "on" else False
        part.public = True if public == "on" else False
        part.rejected = True if rejected == "on" else False
        part.tags = tags

        # Save the changes to the database
        db.session.commit()

        # Return a success response
        message = Markup(
            f'Part updated! <a class="link-success" href="{url_for("views.part", part_number=part_number)}">Go to the part view.</a>'
        )
        flash(message, "success")

    categories = (
        db.session.scalars(
            select(Category)
            .where(Category.parent_id == None)
            .options(joinedload(Category.subcategories))
        )
        .unique()
        .all()
    )
    return render_template("admineditpart.html", part=part, categories=categories)


@views_admin.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == "POST":
        category_id = request.form.get("categoryId", type=int)
        category_name = request.form.get("categoryName")
        parent_id = request.form.get("parentCategory", type=int)
        if category_id is None or category_name is None or parent_id is None:
            flash("Something is missing", "error")
            abort(redirect(url_for(".categories")))
        if parent_id == -1:
            parent_id = None

        if category_id == -1:
            category = Category(name=category_name, parent_id=parent_id)
            db.session.add(category)
        else:
            category = db.session.get(Category, category_id)
            if not category:
                abort(404)
            has_children = db.session.scalar(
                exists(Category.id).where(Category.parent_id == category_id).select()
            )
            if has_children and parent_id is not None:
                flash(
                    "The category is a main category with subcategories and can't be made a subcategory.",
                    "error",
                )
            else:
                category.name = category_name
                category.parent_id = parent_id

        db.session.commit()
        # fall through to GET

    categories = (
        db.session.scalars(
            select(Category)
            .where(Category.parent_id == None)
            .options(joinedload(Category.subcategories))
        )
        .unique()
        .all()
    )
    return render_template("admin-categories.html", categories=categories)

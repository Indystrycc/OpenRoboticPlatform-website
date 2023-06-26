from bleach import clean
from flask import (
    Blueprint,
    Markup,
    abort,
    flash,
    render_template,
    request,
)
from flask_login import current_user, login_required
from functools import wraps

from . import db
from .models import File, Part, User

views_admin = Blueprint("views_admin", __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


@views_admin.route("/panel")
@login_required
@admin_required
def panel():
    page = request.args.get("page", 1, type=int)
    per_page = 20
    parts = (
        db.session.query(Part, User.username)
        .join(User, User.id == Part.user_id)
        .with_entities(Part, User.username)
        .paginate(page=page, per_page=per_page)
    )
    return render_template("adminpanel.html", user=current_user, parts=parts)


@views_admin.route("/editpart:<int:part_number>", methods=["GET", "POST"])
@login_required
@admin_required
def editPart(part_number):
    if request.method == "POST":
        name = clean(request.form.get("name"))
        description = clean(request.form.get("description"))
        category = clean(request.form.get("category"))
        tags = clean(request.form.get("tags"))
        verified = request.form.get("verified")
        public = request.form.get("public")
        rejected = request.form.get("rejected")
        featured = request.form.get("featured")
        category = request.form.get("category")

        # Update the part with the new values using the provided part_id and updated_values
        part = Part.query.get(part_number)
        if part:
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
                f'Part updated! <a href="/part:{part_number}">Go to the part view.</a>'
            )
            flash(message, "success")
        else:
            flash(f"Part {part_number} was not found!", "error")
    part = Part.query.filter_by(id=part_number).first()
    return render_template("admineditpart.html", user=current_user, part=part)

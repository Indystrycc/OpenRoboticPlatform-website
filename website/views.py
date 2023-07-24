import mimetypes
import os
import uuid
from pathlib import Path
from datetime import datetime, timedelta

import MySQLdb.constants.ER as mysql_errors
from bleach import clean
from flask import (
    Blueprint,
    Markup,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

from . import compression_process, db
from .compression import compress_uploads
from .models import Category, File, Part, User, View

ALLOWED_IMAGE_MIME = ["image/png", "image/jpeg"]
views = Blueprint("views", __name__)


@views.route("/")
def home():
    parts = (
        Part.query.filter_by(rejected=False).order_by(Part.date.desc()).limit(10).all()
    )
    return render_template("home.html", user=current_user, parts=parts)


@views.route("/library")
def library():
    page = request.args.get("page", 1, type=int)
    per_page = 20
    search_query = request.args.get("search", "")
    sort_option = request.args.get("sort", "date_desc")
    selected_category = int(request.args.get("category", "-1"))
    verified_only = request.args.get("v", "")

    categories = (
        db.session.scalars(
            select(Category)
            .where(Category.parent_id == None)
            .options(joinedload(Category.subcategories))
        )
        .unique()
        .all()
    )

    if search_query:
        parts = Part.query.filter(
            Part.name.icontains(search_query, autoescape=True)
            | Part.description.icontains(search_query, autoescape=True)
            | Part.tags.icontains(search_query, autoescape=True)
        ).filter_by(rejected=False)
    else:
        parts = Part.query.filter_by(rejected=False)

    if verified_only:
        parts = parts.filter_by(verified=True)

    if selected_category != -1:
        if any(category.id == selected_category for category in categories):
            category_group = next(
                c.subcategories for c in categories if c.id == selected_category
            )
            category_ids = [category.id for category in category_group]
            parts = parts.filter(Part.category.in_(category_ids))
        else:
            parts = parts.filter_by(category=selected_category)

    if sort_option == "date_asc":
        parts = parts.order_by(Part.date.asc())
    elif sort_option == "popularity":
        parts = parts.order_by(Part.downloads.desc())
    else:
        parts = parts.order_by(Part.date.desc())

    parts = parts.paginate(page=page, per_page=per_page)
    return render_template(
        "library.html",
        user=current_user,
        parts=parts,
        sort_option=sort_option,
        categories=categories,
        selected_category=selected_category,
        verified_only=verified_only,
    )


@views.route("/account")
@login_required
def account():
    recent_parts = (
        Part.query.filter_by(user_id=current_user.id)
        .order_by(Part.date.desc())
        .limit(5)
        .all()
    )
    return render_template("account.html", user=current_user, recent_parts=recent_parts)


@views.route("/accountsettings", methods=["GET", "POST"])
@login_required
def accountsettings():
    if request.method == "POST":
        previous_image = None
        new_image = None
        image = request.files.get("image")
        description = clean(request.form.get("description"))
        link_github = clean(request.form.get("name_github"))
        link_youtube = clean(request.form.get("name_youtube"))
        link_instagram = clean(request.form.get("name_instagram"))
        current_user.description = description
        current_user.name_github = link_github
        current_user.name_youtube = link_youtube
        current_user.name_instagram = link_instagram

        if (
            image
            and image.filename
            and mimetypes.guess_type(image.filename)[0] in ALLOWED_IMAGE_MIME
        ):
            previous_image = current_user.image
            new_image, image_path = save_profile_image(image, current_user.username)
            if os.path.getsize(image_path) > 5 * 1024 * 1024:
                delete_profile_image(new_image)
                db.session.rollback()
                flash("The image is too large", "error")
                return redirect(url_for("views.accountsettings"))
            current_user.image = new_image

        try:
            db.session.commit()
        except:
            if new_image:
                delete_profile_image(new_image)
            flash("One of the inputs was too long.", "error")
            return redirect(url_for("views.accountsettings"))

        if previous_image:
            delete_profile_image(previous_image)

        message = Markup(
            'Settings saved! <a href="/account" class="link-success">Go to your account.</a>'
        )
        flash(message, "success")
    return render_template(
        "accountsettings.html", user=current_user, image_types=ALLOWED_IMAGE_MIME
    )


@views.route("/part:<int:part_number>")
def part(part_number):
    part: Part | None = Part.query.get(part_number)
    if not part:
        abort(404)
    author: User | None = User.query.get(part.user_id)
    files_list = part.files
    subcategory: Category | None = part.cat
    category = subcategory.name
    if subcategory.parent_cat:
        category = subcategory.parent_cat
        category = f"{category.name} - {subcategory.name}"

    ip_address = request.remote_addr
    time_delta = datetime.utcnow() - timedelta(hours=3)
    view_count_check: View | None = View.query.filter(
        or_(
            View.ip == ip_address,
            View.user_id == current_user.id if current_user.is_authenticated else False,
        ),
        View.part_id == part_number,
        View.event_date >= time_delta,
    ).all()

    if not view_count_check:
        part.views = int(part.views) + 1
        db.session.commit()
    if current_user.is_authenticated:
        new_view = View(user_id=current_user.id, ip=ip_address, part_id=part_number)
    else:
        new_view = View(user_id=None, ip=ip_address, part_id=part_number)
    db.session.add(new_view)
    db.session.commit()

    return render_template(
        "part.html",
        part=part,
        user=current_user,
        files_list=files_list,
        author=author,
        category=category,
    )


@views.route("/designrules")
def designRules():
    return render_template("design-rules.html", user=current_user)


@views.route("/showcase")
def showcase():
    return render_template("showcase.html", user=current_user)


@views.route("/addpart", methods=["GET", "POST"])
@login_required
def addPart():
    ALLOWED_PART_EXTENSIONS = [".3mf", ".stl", ".step", ".dxf"]
    if request.method == "POST":
        # Retrieve the form data
        name = clean(request.form.get("name"))
        description = clean(request.form.get("description"))
        category = clean(request.form.get("category"))
        tags = clean(request.form.get("tags"))
        image = request.files.get("image")
        files = request.files.getlist("files")

        # Validate the form data (add your validation logic here)
        if not name or not description or not category or not image or len(files) == 0:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("views.addPart"))

        if len(files) > 20:
            flash("Too many files.", "error")
            return redirect(url_for("views.addPart"))

        # Save the part details to the database
        part = Part(
            name=name,
            description=description,
            category=category,
            tags=tags,
            user_id=current_user.id,
        )
        db.session.add(part)
        try:
            db.session.flush()
        except IntegrityError as e:
            if (
                e.orig.args[0] == mysql_errors.NO_REFERENCED_ROW_2
                or e.orig.args[0] == mysql_errors.NO_REFERENCED_ROW
            ):
                flash("Selected category does not exist.", "error")
                db.session.rollback()
                return redirect(url_for("views.addPart"))
            else:
                raise

        if part.cat.parent_id is None:
            flash("Part must be assigned to one of the subcategories.", "error")
            db.session.rollback()
            return redirect(url_for("views.addPart"))

        # Process and save the image
        if (
            not image
            or mimetypes.guess_type(image.filename)[0] not in ALLOWED_IMAGE_MIME
        ):
            db.session.rollback()
            return abort(400)
        image_filename, image_path = save_image(image, part.id, current_user.username)
        if os.path.getsize(image_path) > 5 * 1024 * 1024:
            delete_part_uploads(part.id, current_user.username)
            db.session.rollback()
            flash(f"The image is too large.", "error")
            return redirect(url_for("views.addPart"))
        part.image = image_filename

        # Process and save the files
        for file in files:
            if os.path.splitext(file.filename)[1] not in ALLOWED_PART_EXTENSIONS:
                delete_part_uploads(part.id, current_user.username)
                db.session.rollback()
                return abort(400)
            file_filename, file_path = save_file(file, part.id, current_user.username)
            if os.path.getsize(file_path) > 10 * 1024 * 1024:
                delete_part_uploads(part.id, current_user.username)
                db.session.rollback()
                flash(f"File {file.filename} is too large.", "error")
                return redirect(url_for("views.addPart"))
            part.file_name = file_filename
            db_file = File(part_id=part.id, file_name=file_filename)
            db.session.add(db_file)
        db.session.commit()

        if compression_process:
            compression_process.submit(compress_uploads, part.id, current_user.username)

        flash("Part added successfully!", "success")
        return redirect(url_for("views.addPart"))
    categories = (
        db.session.scalars(
            select(Category)
            .where(Category.parent_id == None)
            .options(joinedload(Category.subcategories))
        )
        .unique()
        .all()
    )
    # Render the addpart.html template for GET requests
    return render_template(
        "addpart.html",
        user=current_user,
        part_extensions=ALLOWED_PART_EXTENSIONS,
        image_types=ALLOWED_IMAGE_MIME,
        categories=categories,
    )


@views.route("/user:<string:user_name>")
def userView(user_name):
    display_user = User.query.filter_by(username=user_name).first()
    if not display_user:
        abort(404)
    recent_parts = (
        Part.query.filter_by(user_id=display_user.id)
        .order_by(Part.date.desc())
        .limit(10)
        .all()
    )
    return render_template(
        "user.html",
        user=current_user,
        display_user=display_user,
        recent_parts=recent_parts,
    )


def save_image(image, part_id, username):
    # Specify the directory where you want to save the images
    upload_folder = "website/static/uploads/images"

    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Generate a secure filename and save the image to the upload folder
    filename = secure_filename(image.filename)
    ext = os.path.splitext(filename)[1]
    filename = f"part-{username}-{part_id}-{uuid.uuid4()}{ext}"
    save_path = os.path.join(upload_folder, filename)
    image.save(save_path)

    return filename, save_path


def save_profile_image(image, username):
    upload_folder = "website/static/uploads/profile_images"
    filename, file_extension = os.path.splitext(image.filename)
    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Generate a secure filename and save the image to the upload folder
    filename = f"pi-{username}-{uuid.uuid4()}{file_extension}"
    save_path = os.path.join(upload_folder, filename)
    image.save(save_path)

    return filename, save_path


def delete_profile_image(filename: str):
    upload_folder = "website/static/uploads/profile_images"

    try:
        image_path = os.path.join(upload_folder, filename)
        os.remove(image_path)
    except FileNotFoundError:
        pass


def save_file(file, part_id, username):
    upload_folder = "website/static/uploads/files"

    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Generate a secure filename and save the file to the upload folder
    filename = secure_filename(file.filename)
    filename = f"{username}-{part_id}-{filename}"
    if len(filename) > 100:
        f_name, f_ext = os.path.splitext(filename)
        # 97, because there will be (at most) 2 digits and '~'
        trunc_len = 97 - len(f_ext)
        assert trunc_len > 0
        f_name = f_name[:trunc_len]
        for i in range(1, 21):
            final_name = f"{f_name}~{i}{f_ext}"
            full_path = os.path.join(upload_folder, final_name)
            if not os.path.exists(full_path):
                filename = final_name
                break

    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)

    return filename, save_path


def delete_part_uploads(part_id: int, username: str):
    image_uploads_dir = Path("website/static/uploads/images")
    file_uploads_dir = Path("website/static/uploads/files")

    for img in image_uploads_dir.glob(f"part-{username}-{part_id}-*"):
        img.unlink()

    for file in file_uploads_dir.glob(f"{username}-{part_id}-*"):
        file.unlink()

import mimetypes
import os
import uuid
from pathlib import Path

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
    jsonify,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import compression_process, db
from .compression import compress_uploads
from .models import File, Part, User

ALLOWED_IMAGE_MIME = ["image/png", "image/jpeg"]
views = Blueprint("views", __name__)


@views.route("/")
def home():
    parts = (
        Part.query.filter_by(rejected=False).order_by(Part.date.desc()).limit(5).all()
    )
    return render_template("home.html", user=current_user, parts=parts)


@views.route("/library")
def library():
    page = request.args.get("page", 1, type=int)
    per_page = 20
    search_query = request.args.get("search", "")

    # Filter parts based on search query
    if search_query:
        parts = Part.query.filter(
            Part.name.icontains(search_query, autoescape=True)
            | Part.description.icontains(search_query, autoescape=True)
            | Part.tags.icontains(search_query, autoescape=True)
        ).filter_by(rejected=False)
    else:
        parts = Part.query.filter_by(rejected=False)

    parts = parts.paginate(page=page, per_page=per_page)
    return render_template("library.html", user=current_user, parts=parts)


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
        image = request.files.get("image")
        description = clean(request.form.get("description"))
        link_github = clean(request.form.get("name_github"))
        link_youtube = clean(request.form.get("name_youtube"))
        link_instagram = clean(request.form.get("name_instagram"))
        current_user.description = description[:75]
        current_user.name_github = link_github
        current_user.name_youtube = link_youtube
        current_user.name_instagram = link_instagram

        if (
            image
            and image.filename
            and mimetypes.guess_type(image.filename)[0] in ALLOWED_IMAGE_MIME
        ):
            previous_image = current_user.image
            current_user.image = save_profile_image(image, current_user.username)

            if previous_image:
                delete_profile_image(previous_image)

        db.session.commit()
        message = Markup('Settings saved!, <a href="/account">Go to your account.</a>')
        flash(message, "success")
    return render_template(
        "accountsettings.html", user=current_user, image_types=ALLOWED_IMAGE_MIME
    )


@views.route("/part:<int:part_number>")
def part(part_number):
    part = Part.query.filter_by(id=part_number).first()
    author = User.query.filter_by(id=part.user_id).first()
    files_list = File.query.filter_by(part_id=part_number).all()
    if not part:
        abort(404)

    return render_template(
        "part.html", part=part, user=current_user, files_list=files_list, author=author
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
    ALLOWED_PART_EXTENSIONS = [".3mf", ".stl", ".step"]
    if request.method == "POST":
        # Retrieve the form data
        name = clean(request.form.get("name"))
        description = clean(request.form.get("description"))
        category = clean(request.form.get("category"))
        tags = clean(request.form.get("tags"))
        image = request.files.get("image")
        files = request.files.getlist("files")

        # Validate the form data (add your validation logic here)
        if not name or not description or not category:
            flash("Please fill in all required fields.", "error")
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
        db.session.flush()

        # Process and save the image
        if (
            not image
            or mimetypes.guess_type(image.filename)[0] not in ALLOWED_IMAGE_MIME
        ):
            db.session.rollback()
            return abort(400)
        image_filename = save_image(image, part.id, current_user.username)
        part.image = image_filename

        # Process and save the files
        for file in files:
            if os.path.splitext(file.filename)[1] not in ALLOWED_PART_EXTENSIONS:
                delete_part_uploads(part.id, current_user.username)
                db.session.rollback()
                return abort(400)
            file_filename = save_file(file, part.id, current_user.username)
            part.file_name = file_filename
            db_file = File(part_id=part.id, file_name=file_filename)
            db.session.add(db_file)
        db.session.commit()

        if compression_process:
            compression_process.submit(compress_uploads, part.id, current_user.username)

        flash("Part added successfully!", "success")
        return redirect(url_for("views.addPart"))

    # Render the addpart.html template for GET requests
    return render_template(
        "addpart.html",
        user=current_user,
        part_extensions=ALLOWED_PART_EXTENSIONS,
        image_types=ALLOWED_IMAGE_MIME,
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

    return filename


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

    return filename


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
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)

    return filename


def delete_part_uploads(part_id: int, username: str):
    image_uploads_dir = Path("website/static/uploads/images")
    file_uploads_dir = Path("website/static/uploads/files")

    for img in image_uploads_dir.glob(f"part-{username}-{part_id}-*"):
        img.unlink()

    for file in file_uploads_dir.glob(f"{username}-{part_id}-*"):
        file.unlink()

import mimetypes
import os
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

import MySQLdb.constants.ER as mysql_errors
import requests
from bleach import clean
from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.typing import ResponseReturnValue
from flask_login import login_required
from markupsafe import Markup
from PIL import Image, UnidentifiedImageError
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from . import (
    compression_process,
    csp_youtube_ext,
    db,
    default_csp,
    disable_COEP,
    talisman,
)
from .compression import compress_uploads
from .models import Category, File, Part, Stats, User, View, Comment
from .secrets_manager import MAILERLITE_API_KEY
from .session_utils import get_session, get_user
from .thumbnailer import create_thumbnails, load_check_image
from .utils import extend_talisman_csp

ALLOWED_IMAGE_MIME = ["image/png", "image/jpeg"]
ALLOWED_PART_EXTENSIONS = [".3mf", ".stl", ".step", ".dxf", ".scad"]
views = Blueprint("views", __name__)


@views.route("/")
@talisman(content_security_policy=extend_talisman_csp(default_csp, csp_youtube_ext))
@disable_COEP
def home() -> ResponseReturnValue:
    parts = db.session.scalars(
        select(Part).where(Part.rejected == False).order_by(Part.date.desc()).limit(10)
    )
    stats = db.session.get(Stats, 1)

    return render_template("home.html", parts=parts, stats=stats)


@views.route("/library")
def library() -> ResponseReturnValue:
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

    parts_query = select(Part).where(Part.rejected == False)
    if search_query:
        parts_query = parts_query.where(
            or_(
                Part.name.icontains(search_query, autoescape=True),
                Part.description.icontains(search_query, autoescape=True),
                Part.tags.icontains(search_query, autoescape=True),
            )
        )

    if verified_only:
        parts_query = parts_query.where(Part.verified == True)

    if selected_category != -1:
        if any(category.id == selected_category for category in categories):
            category_group = next(
                c.subcategories for c in categories if c.id == selected_category
            )
            category_ids = [category.id for category in category_group]
            parts_query = parts_query.where(Part.category.in_(category_ids))
        else:
            parts_query = parts_query.where(Part.category == selected_category)

    if sort_option == "date_asc":
        parts_query = parts_query.order_by(Part.date.asc())
    elif sort_option == "popularity":
        parts_query = parts_query.order_by(Part.views.desc())
    else:
        parts_query = parts_query.order_by(Part.date.desc())

    parts = db.paginate(parts_query, per_page=per_page)
    return render_template(
        "library.html",
        parts=parts,
        sort_option=sort_option,
        categories=categories,
        selected_category=selected_category,
        verified_only=verified_only,
    )


@views.route("/account")
@login_required
def account() -> ResponseReturnValue:
    current_user = get_user()
    recent_parts = db.session.scalars(
        select(Part)
        .where(Part.user_id == current_user.id)
        .order_by(Part.date.desc())
        .limit(5)
    )
    stats, user_parts, user_contribution = calculate_user_contribution(current_user.id)
    total_parts = stats.total_parts if stats and stats.total_parts else 0

    return render_template(
        "account.html",
        recent_parts=recent_parts,
        total_parts=total_parts,
        user_parts=user_parts,
        user_contribution=user_contribution,
    )


@views.route("/accountsettings", methods=["GET", "POST"])
@login_required
def accountsettings() -> ResponseReturnValue:
    if request.method == "POST":
        current_user = get_user()
        previous_image = None
        new_image = None
        image = request.files.get("image")
        description = clean(
            request.form.get("description", current_user.description or "")
        )
        link_github = clean(
            request.form.get("name_github", current_user.name_github or "")
        )
        link_youtube = clean(
            request.form.get("name_youtube", current_user.name_youtube or "")
        )
        link_instagram = clean(
            request.form.get("name_instagram", current_user.name_instagram or "")
        )
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
            new_image, image_path = save_profile_image(
                image, image.filename, current_user.username
            )
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
    return render_template("accountsettings.html", image_types=ALLOWED_IMAGE_MIME)


@views.route("/part:<int:part_number>", methods=["GET", "POST"])
def part(part_number: int) -> ResponseReturnValue:
    current_user = get_session()
    
    # Handle comment submission
    if request.method == "POST" and isinstance(current_user, User):
        content = clean(request.form.get("content", ""))
        parent_id = request.form.get("parent_id", type=int)
        
        if content:
            comment = Comment(
                content=content,
                user_id=current_user.id,
                part_id=part_number,
                parent_id=parent_id
            )
            db.session.add(comment)
            db.session.commit()
            flash("Comment added successfully!", "success")
        else:
            flash("Comment cannot be empty", "error")

    # A few substrings which can be often found in web crawlers
    BOT_UA_FRAGMENTS = ["bot", "crawler", "spider", "slurp", "spyder"]
    part = db.session.get(Part, part_number)
    if not part:
        abort(404)
    author = part.author
    files_list = part.files
    subcategory = part.cat
    category = subcategory.name
    if subcategory.parent_cat:
        category = subcategory.parent_cat
        category = f"{category.name} - {subcategory.name}"

    ip_address = request.remote_addr
    time_delta = datetime.now(UTC) - timedelta(hours=3)
    if isinstance(current_user, User):
        same_user_filter = or_(View.ip == ip_address, View.user_id == current_user.id)
    else:
        same_user_filter = View.ip == ip_address
    view_count_check = db.session.scalar(
        select(View).where(
            same_user_filter,
            View.part_id == part_number,
            View.event_date >= time_delta,
        )
    )

    ua_lower = request.user_agent.string.lower()
    if not view_count_check and not any(
        bot_ua_fragment in ua_lower for bot_ua_fragment in BOT_UA_FRAGMENTS
    ):
        part.views = int(part.views) + 1
        if isinstance(current_user, User):
            new_view = View(user_id=current_user.id, ip=ip_address, part_id=part_number)
        else:
            new_view = View(user_id=None, ip=ip_address, part_id=part_number)
        db.session.add(new_view)
        db.session.commit()

    # DB does not store timezone, but it's always UTC
    if part.last_modified is not None:
        part.last_modified = part.last_modified.replace(tzinfo=UTC)

    # Get top-level comments
    comments = (
        db.session.scalars(
            select(Comment)
            .where(Comment.part_id == part_number, Comment.parent_id == None)
            .order_by(Comment.date.desc())
            .options(
                joinedload(Comment.author),
                joinedload(Comment.replies).joinedload(Comment.author)
            )
        )
        .unique()
        .all()
    )

    return render_template(
        "part.html",
        part=part,
        files_list=files_list,
        author=author,
        category=category,
        comments=comments,
    )


@views.route("/designrules")
def designRules() -> ResponseReturnValue:
    return render_template("design-rules.html")


@views.route("/showcase")
def showcase() -> ResponseReturnValue:
    return render_template("showcase.html")


@views.route("/addpart", methods=["GET", "POST"])
@login_required
def addPart() -> ResponseReturnValue:
    current_user = get_user()
    if not current_user.confirmed:
        flash("You have to confirm your email before uploading a part.", "error")
        return redirect(url_for("views.account"))

    if request.method == "POST":
        # Retrieve the form data
        name = clean(request.form.get("name", ""))
        description = clean(request.form.get("description", ""))
        category = request.form.get("category", type=int)
        tags = clean(request.form.get("tags", ""))
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
            # The image path can only be generated if part id is known
            image="",
        )
        db.session.add(part)
        try:
            db.session.flush()
        except IntegrityError as e:
            if e.orig and (
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
        image_filename = save_image_and_validate(
            part, image, True, current_user.username
        )
        if not image_filename:
            return redirect(url_for("views.addPart"))
        part.image = image_filename

        # Process and save the files
        for file in files:
            if (
                not file.filename
                or os.path.splitext(file.filename)[1] not in ALLOWED_PART_EXTENSIONS
            ):
                delete_part_uploads(part.id, current_user.username)
                abort(400)
            file_filename, file_path = save_file(
                file, file.filename, part.id, current_user.username
            )
            if os.path.getsize(file_path) > 10 * 1024 * 1024:
                delete_part_uploads(part.id, current_user.username)
                flash(f"File {file.filename} is too large.", "error")
                return redirect(url_for("views.addPart"))
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
        part_extensions=ALLOWED_PART_EXTENSIONS,
        image_types=ALLOWED_IMAGE_MIME,
        categories=categories,
    )


@views.route("/part:<int:part_number>/edit", methods=["GET", "POST"])
@login_required
def edit_part(part_number: int) -> ResponseReturnValue:
    current_user = get_user()
    part = db.session.get(Part, part_number)
    if part is None:
        abort(404)
    if part.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        upload_folder = "website/static/uploads/files"
        name = clean(request.form.get("name", part.name))
        description = clean(request.form.get("description", part.description))
        tags = clean(request.form.get("tags", part.tags))
        if not name or not description:
            flash("Name and descriptio are required.", "error")
            return redirect(url_for(".edit_part", part_number=part.id))

        # Replace part image if a new one was sent
        image = request.files.get("image")
        old_image = part.image
        image_filename = None
        if image:
            image_filename = save_image_and_validate(
                part, image, False, current_user.username
            )
            if not image_filename:
                return redirect(url_for(".edit_part", part_number=part.id))
            part.image = image_filename

        def img_cleanup() -> None:
            if image_filename:
                delete_part_image(image_filename)

        deleted_files = request.form.getlist("removedFiles")
        for df in deleted_files:
            exists = False
            for pf in part.files:
                if pf.file_name == df:
                    exists = True
                    db.session.delete(pf)
                    break
            if not exists:
                flash(f"File {df} does not exist.", "error")
                return redirect(url_for(".edit_part", part_number=part.id))

        # Flush changes to DB before adding new files or we'll get duplicate error
        db.session.flush()

        # Process and save new files
        new_files = []
        for file in request.files.getlist("files"):
            if not file:
                # No file selected
                continue
            if (
                not file.filename
                or os.path.splitext(file.filename)[1] not in ALLOWED_PART_EXTENSIONS
            ):
                delete_part_uploads(part.id, current_user.username, tmp_only=True)
                img_cleanup()
                abort(400)
            file_filename, file_path = save_file(
                file, file.filename, part.id, current_user.username, tmp=True
            )
            if os.path.getsize(file_path) > 10 * 1024 * 1024:
                delete_part_uploads(part.id, current_user.username, tmp_only=True)
                img_cleanup()
                flash(f"File {file.filename} is too large.", "error")
                return redirect(url_for(".edit_part", part_number=part.id))
            final_filename = file_filename[:-5]  # remove __tmp
            if (
                os.path.isfile(os.path.join(upload_folder, final_filename))
                and final_filename not in deleted_files
            ):
                delete_part_uploads(part.id, current_user.username, tmp_only=True)
                img_cleanup()
                flash(
                    f"File {file.filename} already exists and is not marked for deletion.",
                    "error",
                )
                return redirect(url_for(".edit_part", part_number=part.id))
            db_file = File(part_id=part.id, file_name=final_filename)
            db.session.add(db_file)
            new_files.append(final_filename)

        part.name = name
        part.description = description
        part.tags = tags
        part.last_modified = datetime.now(UTC)

        # Everything is ok, apply filesystem (and db) changes
        if image:
            delete_part_image(old_image)

        for df in deleted_files:
            f_path = os.path.join(upload_folder, df)
            os.unlink(f_path)

        upload_dir = Path(upload_folder)
        for nf in new_files:
            ext = os.path.splitext(nf)[1]
            f = upload_dir / f"{nf}__tmp"
            f.rename(f.with_suffix(ext))

        db.session.commit()

        return redirect(url_for(".part", part_number=part.id))

    return render_template(
        "edit-part.html",
        part=part,
        part_extensions=ALLOWED_PART_EXTENSIONS,
        image_types=ALLOWED_IMAGE_MIME,
    )


@views.route("/user:<string:user_name>")
def userView(user_name: str) -> ResponseReturnValue:
    display_user = db.session.scalar(select(User).where(User.username == user_name))
    if not display_user:
        abort(404)
    recent_parts = db.session.scalars(
        select(Part)
        .where(Part.user_id == display_user.id)
        .order_by(Part.date.desc())
        .limit(10)
    )
    stats, user_parts, user_contribution = calculate_user_contribution(display_user.id)
    total_parts = stats.total_parts if stats and stats.total_parts else 0
    return render_template(
        "user.html",
        display_user=display_user,
        recent_parts=recent_parts,
        total_parts=total_parts,
        user_contribution=user_contribution,
        user_parts=user_parts,
    )


@views.route("/newsletterAdd", methods=["POST"])
def newsletterAdd() -> ResponseReturnValue:
    success, message = save_new_subscriber(clean(request.form.get("email", "")))
    return jsonify({"success": success})


def save_image(image: FileStorage, part_id: int, username: str) -> tuple[str, str]:
    # Specify the directory where you want to save the images
    upload_folder = "website/static/uploads/images"
    thumbs_dir = os.path.join(upload_folder, "thumbs")

    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Load the image and check if it is correct (PNG or JPEG with minimal dimensions)
    img = load_check_image(image)

    assert image.filename is not None
    # Generate a secure filename and save the image to the upload folder
    filename = secure_filename(image.filename)
    ext = os.path.splitext(filename)[1]
    filename = f"part-{username}-{part_id}-{uuid.uuid4()}{ext}"
    save_path = os.path.join(upload_folder, filename)
    # The stream was read by PIL and needs to be "rewound" before saving (otherwise we won't get the full file)
    image.stream.seek(0)
    image.save(save_path)

    # Generate and save thumbnails
    create_thumbnails(img, thumbs_dir, filename)
    img.close()

    return filename, save_path


def save_image_and_validate(
    part: Part, image: FileStorage, delete_all: bool, username: str
) -> str | None:
    if (
        not image
        or not image.filename
        or mimetypes.guess_type(image.filename)[0] not in ALLOWED_IMAGE_MIME
    ):
        abort(400)
    try:
        image_filename, image_path = save_image(image, part.id, username)
    except ValueError as e:
        flash(e.args[0], "error")
        return None
    except UnidentifiedImageError:
        flash("The image is not a proper JPEG or PNG file.", "error")
        return None
    except Image.DecompressionBombError:
        flash("The image has more then 64 MP. Please use a smaller image.", "error")
        return None
    if os.path.getsize(image_path) > 5 * 1024 * 1024:
        if delete_all:
            delete_part_uploads(part.id, username)
        else:
            delete_part_image(image_filename)
        flash(f"The image is too large.", "error")
        return None

    return image_filename


def save_profile_image(
    image: FileStorage, filename: str, username: str
) -> tuple[str, str]:
    upload_folder = "website/static/uploads/profile_images"
    filename, file_extension = os.path.splitext(filename)
    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Generate a secure filename and save the image to the upload folder
    filename = f"pi-{username}-{uuid.uuid4()}{file_extension}"
    save_path = os.path.join(upload_folder, filename)
    image.save(save_path)

    return filename, save_path


def delete_part_image(image_filename: str) -> None:
    image_uploads_dir = Path("website/static/uploads/images")
    filename_base = os.path.splitext(image_filename)[0]
    for img in image_uploads_dir.rglob(filename_base + ".*"):
        img.unlink()


def delete_profile_image(filename: str) -> None:
    upload_folder = "website/static/uploads/profile_images"

    try:
        image_path = os.path.join(upload_folder, filename)
        os.remove(image_path)
    except FileNotFoundError:
        pass


def save_file(
    file: FileStorage, filename: str, part_id: int, username: str, tmp: bool = False
) -> tuple[str, str]:
    upload_folder = "website/static/uploads/files"

    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Generate a secure filename and save the file to the upload folder
    filename = secure_filename(filename)
    filename = f"{username}-{part_id}-{filename}"
    if tmp:
        filename += "__tmp"
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


def delete_part_uploads(part_id: int, username: str, tmp_only: bool = False) -> None:
    image_uploads_dir = Path("website/static/uploads/images")
    file_uploads_dir = Path("website/static/uploads/files")

    if not tmp_only:
        for img in image_uploads_dir.rglob(f"part-{username}-{part_id}-*"):
            img.unlink()

    suffix = ""
    if tmp_only:
        suffix += "__tmp"
    for file in file_uploads_dir.glob(f"{username}-{part_id}-*{suffix}"):
        file.unlink()


def calculate_user_contribution(id: uuid.UUID) -> tuple[Stats | None, int, float]:
    stats = db.session.get(Stats, 1)
    user_parts = (
        db.session.scalar(
            select(func.count()).select_from(Part).where(Part.user_id == id)
        )
        or 0
    )
    total_parts = stats.total_parts if stats and stats.total_parts else 0
    user_contribution = round(
        (user_parts / total_parts) * 100 if total_parts > 0 else 0, 2
    )
    return stats, user_parts, user_contribution


def save_new_subscriber(email: str) -> tuple[bool, requests.Response]:
    url = "https://connect.mailerlite.com/api/subscribers"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {MAILERLITE_API_KEY}",
    }

    data = {
        "email": email,
        "groups": ["95057407892260283"],
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        return True, response
    else:
        return False, response

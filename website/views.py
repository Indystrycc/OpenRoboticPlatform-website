from flask import Blueprint, render_template, request, redirect, flash, url_for, abort, Markup
from flask_login import login_required, current_user
from .models import Part, File, User
from . import db
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import Pagination
from bleach import clean
import random

views = Blueprint('views', __name__)

@views.route('/')
def home():
    parts = Part.query.order_by(Part.date.desc()).limit(5).all()
    return render_template("home.html", user = current_user, parts = parts)

@views.route('/library')
def library():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    search_query = request.args.get('search', '')

    # Filter parts based on search query
    if search_query:
        parts = Part.query.filter(Part.name.icontains(search_query, autoescape=True) | Part.description.icontains(search_query, autoescape=True) | Part.tags.icontains(search_query, autoescape=True))
    else:
        parts = Part.query

    parts = parts.paginate(page=page, per_page=per_page)
    return render_template('library.html', user=current_user, parts=parts)

@views.route('/account')
@login_required
def account():
    recent_parts = Part.query.filter_by(user_id=current_user.id).order_by(Part.date.desc()).limit(5).all()
    return render_template("account.html", user = current_user, recent_parts = recent_parts)

@views.route('/accountsettings', methods=['GET', 'POST'])
@login_required
def accountsettings():
    if request.method == 'POST':
        image = request.files.get('image')
        description = clean(request.form.get('description'))
        link_github = clean(request.form.get('name_github'))
        link_youtube = clean(request.form.get('name_youtube'))
        link_instagram = clean(request.form.get('name_instagram'))
        current_user.description = description[:75]
        current_user.name_github = link_github
        current_user.name_youtube = link_youtube
        current_user.name_instagram = link_instagram

        if image and image.filename != '':
            current_user.image = save_profile_image(image, current_user.id)

        db.session.commit()
        message = Markup('Settings saved!, <a href="/account">Go to your account.</a>')
        flash(message, 'success')
    return render_template("accountsettings.html", user = current_user)

@views.route('/part:<int:part_number>')
def part(part_number):
    part = Part.query.filter_by(id=part_number).first()
    author = User.query.filter_by(id=part.user_id).first()
    files_list = File.query.filter_by(part_id=part_number).all()
    if not part:
        abort(404)
        
    return render_template('part.html', part=part, user=current_user, files_list=files_list, author=author)

@views.route('/designrules')
def designRules():
    return render_template("design-rules.html", user = current_user)

@views.route('/showcase')
def showcase():
    return render_template("showcase.html", user = current_user)

@views.route('/addpart', methods=['GET', 'POST'])
@login_required
def addPart():
    if request.method == 'POST':
        # Retrieve the form data
        name = clean(request.form.get('name'))
        description = clean(request.form.get('description'))
        category = clean(request.form.get('category'))
        tags = clean(request.form.get('tags'))
        image = request.files.get('image')
        files = request.files.getlist('files')

        # Validate the form data (add your validation logic here)
        if not name or not description or not category:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('views.addPart'))

        # Save the part details to the database
        part = Part(name=name, description=description, category=category, tags=tags, user_id=current_user.id)
        db.session.add(part)
        db.session.commit()

        # Process and save the image
        if image:
            image_filename = save_image(image, part.id, current_user.id)
            part.image = image_filename

        # Process and save the files
        for file in files:
            file_filename = save_file(file, part.id, current_user.id)  # Implement the save_file function
            part.file_name = file_filename
            db_file = File(part_id = part.id, file_name = file_filename)
            db.session.add(db_file)
            db.session.commit()
        db.session.commit()

        flash('Part added successfully!', 'success')
        return redirect(url_for('views.addPart'))

    # Render the addpart.html template for GET requests
    return render_template('addpart.html', user=current_user)



def save_image(image, part_id, user_id):
    # Specify the directory where you want to save the images
    upload_folder = 'website/static/uploads/images'

    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Generate a secure filename and save the image to the upload folder
    filename = secure_filename(image.filename)
    filename = f'part_{user_id}_{part_id}_{"%030x" % random.randrange(16**20)}'
    save_path = os.path.join(upload_folder, filename)
    image.save(save_path)

    # Return the saved filename or unique identifier
    return filename

def save_profile_image(image, user_id):
    # Specify the directory where you want to save the images
    upload_folder = 'website/static/uploads/profile_images'

    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Generate a secure filename and save the image to the upload folder
    filename = secure_filename(image.filename)
    filename = f'pi_{user_id}_{"%030x" % random.randrange(16**20)}'
    save_path = os.path.join(upload_folder, filename)
    image.save(save_path)

    # Return the saved filename or unique identifier
    return filename

def save_file(file, part_id, user_id):
    # Specify the directory where you want to save the files
    upload_folder = 'website/static/uploads/files'

    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Generate a secure filename and save the file to the upload folder
    filename = secure_filename(file.filename)
    filename = f'part_{user_id}_{part_id}_{filename}'
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)

    # Return the saved filename or unique identifier
    return filename

from flask import Blueprint, render_template, request, redirect, flash, url_for, abort
from flask_login import login_required, current_user
from .models import Part, File
from . import db
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/')
def home():
    posts = [
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': '300mm plate',
            'views': 10,
            'likes': 5
        },
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': '200mm plate',
            'views': 5,
            'likes': 0
        },
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': '150mm plate',
            'views': 7,
            'likes': 2
        },
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': 'Jetson Nano holder',
            'views': 59,
            'likes': 20
        },
         {
            'image': 'static/assets/img/robot2.jpg',
            'title': '300mm plate',
            'views': 10,
            'likes': 5
        }
    ]
    return render_template("home.html", user = current_user, newest_parts = posts)

@views.route('/library')
def library():
    posts = [
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': '300mm plate',
            'views': 10,
            'likes': 5
        },
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': '200mm plate',
            'views': 5,
            'likes': 0
        },
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': '150mm plate',
            'views': 7,
            'likes': 2
        },
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': 'Jetson Nano holder',
            'views': 59,
            'likes': 20
        },
         {
            'image': 'static/assets/img/robot2.jpg',
            'title': '300mm plate',
            'views': 10,
            'likes': 5
        },
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': '200mm plate',
            'views': 5,
            'likes': 0
        },
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': '150mm plate',
            'views': 7,
            'likes': 2
        },
        {
            'image': 'static/assets/img/robot2.jpg',
            'title': 'Jetson Nano holder',
            'views': 59,
            'likes': 20
        }
    ]
    return render_template("library.html", user = current_user, posts=posts)

@views.route('/account')
@login_required
def account():
    recent_parts = Part.query.filter_by(user_id=current_user.id).order_by(Part.date.desc()).limit(5).all()
    return render_template("account.html", user = current_user, recent_parts = recent_parts)

@views.route('/part:<int:part_number>')
def part(part_number):
    part = Part.query.filter_by(id=part_number).first()
    files_list = File.query.filter_by(part_id=part_number).all()
    for f in files_list:
        print(f.file_name)
    if not part:
        abort(404)
    
    return render_template('part.html', part=part, user=current_user, files_list2=files_list)

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
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        tags = request.form.get('tags')
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
            print('saving image')
            image_filename = save_image(image, part.id, current_user.id)
            part.image = image_filename

        # Process and save the files
        for file in files:
            print('saving file')
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
    filename = f'part_{user_id}_{part_id}_{filename}'
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

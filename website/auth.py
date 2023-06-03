from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('No user registered with this email', category='error')
    return render_template('login.html', user = current_user)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email is already registered', category='error')
        elif len(username) < 4:
            flash('Username must be longer than 4 characters.', category='error')
        elif len(username) > 20:
            flash('Username must be shorter than 20 characters', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        else:
            new_user_data = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user_data)
            db.session.commit()
            login_user(new_user_data, remember=True)
            flash('Account created sucessfuly!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('signup.html', user = current_user)
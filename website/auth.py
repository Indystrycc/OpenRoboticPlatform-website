from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template('login.html')

@auth.route('logout')
def logout():
    return "<p>logout</p>"

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')

        if len(username) < 4:
            flash('Username must be longer than 4 characters.', category='error')
        elif len(username) > 20:
            flash('Username must be shorter than 20 characters', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        else:
            flash('Account created sucessfuly!', category='success')
        
    return render_template('signup.html')
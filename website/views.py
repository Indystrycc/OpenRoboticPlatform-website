from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user = current_user)

@views.route('/library')
def library():
    return render_template("library.html", user = current_user)

@views.route('/account')
@login_required
def account():
    return render_template("account.html", user = current_user)

@views.route('/part')
def part():
    return render_template("part.html", user = current_user)

@views.route('/designrules')
def designRules():
    return render_template("design-rules.html", user = current_user)

@views.route('/showcase')
def showcase():
    return render_template("showcase.html", user = current_user)
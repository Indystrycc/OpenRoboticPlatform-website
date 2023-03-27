from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/library')
def library():
    return render_template("library.html")

@views.route('/account')
def account():
    return render_template("account.html")

@views.route('/part')
def part():
    return render_template("part.html")
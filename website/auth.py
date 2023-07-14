import re
import sys

import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from MySQLdb.constants.ER import DUP_ENTRY
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User
from .secrets_manager import *

USERNAME_PATTERN = re.compile(r"[\w]+", flags=re.ASCII)

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password", category="error")
        else:
            flash("No user registered with this email", category="error")
    return render_template("login.html", user=current_user)


@auth.route("logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        recaptcha_response = request.form.get("g-recaptcha-response")

        url = "https://www.google.com/recaptcha/api/siteverify"
        data = {"secret": RECAPTCHA_PRIVATE_KEY, "response": recaptcha_response}
        response = requests.post(url, data=data)
        captcha_result = response.json()

        if captcha_result["success"]:
            user = User.query.filter_by(email=email).first()
            if user:
                flash("This email is already registered.", category="error")
            elif len(username) < 4:
                flash("Username must be longer than 4 characters.", category="error")
            elif len(username) > 20:
                flash(
                    "Username must not be longer than 20 characters.", category="error"
                )
            elif not USERNAME_PATTERN.fullmatch(username):
                flash(
                    "Username can contain only alphanumeric characters and '-'.",
                    category="error",
                )
            elif len(password) < 8:
                flash("Password must be at least 8 characters long.", category="error")
            # A completely arbitrary length limit
            elif len(password.encode("utf-8")) > 128:
                flash("Password must not be longer than 128 bytes.", category="error")
            else:
                try:
                    new_user_data = User(
                        email=email,
                        username=username,
                        password=generate_password_hash(
                            password, method="scrypt:131072:8:1"
                        ),
                    )
                    db.session.add(new_user_data)
                    db.session.commit()
                    login_user(new_user_data, remember=True)
                    flash("Account created successfully!", category="success")
                    return redirect(url_for("views.home"))
                except IntegrityError as e:
                    if e.orig.args[0] == DUP_ENTRY:
                        flash("This username is already registered.", category="error")
                    else:
                        print(e, file=sys.stderr)
                        flash(
                            "Something went wrong. Please try again later.",
                            category="error",
                        )
        else:
            flash("CAPTCHA validation failed. Please try again.", category="error")
    return render_template(
        "signup.html", user=current_user, recaptcha_site_key=RECAPTCHA_PUBLIC_KEY
    )

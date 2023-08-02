import base64
import math
import re
import secrets
import sys
from datetime import UTC, datetime, timedelta
from os import getenv

import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from markupsafe import Markup
from MySQLdb.constants.ER import DUP_ENTRY
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from . import csp_captcha, db, production, talisman
from .mailer import send_confirmation_mail
from .models import EmailToken, TokenType, User
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
@talisman(content_security_policy=csp_captcha)
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

        if captcha_result["success"] and (
            getenv("FLASK_ENV") != "production"
            or (captcha_result["score"] >= 0.5 and captcha_result["action"] == "signup")
        ):
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
                    if production:
                        db.session.flush()
                        activation_token = secrets.token_bytes(32)
                        confirmation_url = url_for(
                            ".confirm_email",
                            _scheme="https",
                            _external=True,
                            token_enc=base64.urlsafe_b64encode(activation_token),
                        )
                        saved_token = EmailToken(
                            token=activation_token,
                            token_type=TokenType.mail_confirmation,
                            user_id=new_user_data.id,
                        )
                        db.session.add(saved_token)
                        send_confirmation_mail(username, email, confirmation_url)
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
                except ValueError as e:
                    # Probably invalid email
                    flash("Invalid data provided", "error")
        else:
            flash("CAPTCHA validation failed. Please try again.", category="error")
    return render_template(
        "signup.html", user=current_user, recaptcha_site_key=RECAPTCHA_PUBLIC_KEY
    )


@auth.route("/signup/confirm/<token_enc>")
def confirm_email(token_enc: str):
    token = base64.urlsafe_b64decode(token_enc)
    valid_time = datetime.now(UTC) - timedelta(hours=48)
    matching_token = db.session.scalar(
        select(EmailToken).where(
            EmailToken.token == token,
            EmailToken.token_type == TokenType.mail_confirmation,
            EmailToken.created_on >= valid_time,
        )
    )
    if not matching_token:
        if not current_user.confirmed:
            flash(
                Markup(
                    f'Invalid or expired link. You can request a new activation link on the <a href="{url_for("views.account")}">profile page</a>.'
                ),
                "error",
            )
        else:
            flash("Invalid or expired link.", "error")
        return redirect("/")

    matching_token.user.confirmed = True
    db.session.delete(matching_token)
    db.session.commit()
    flash("Email successfully confirmed. You can now upload parts.")
    return redirect("/")


@auth.route("/signup/resend_mail", methods=["POST"])
@login_required
def resend_confirmation_email():
    if current_user.confirmed:
        flash("Your email has already been confirmed.")
        return redirect(url_for("views.account"))

    saved_token = db.session.scalar(
        select(EmailToken).where(
            EmailToken.user_id == current_user.id,
            EmailToken.token_type == TokenType.mail_confirmation,
        )
    )
    # Allow resending email every 5 minutes
    allowed_after = (
        (saved_token.created_on.replace(tzinfo=UTC) + timedelta(minutes=5))
        if saved_token
        else None
    )
    now = datetime.now(UTC)
    if allowed_after and now <= allowed_after:
        wait = allowed_after - now
        minutes, seconds = divmod(math.ceil(wait.total_seconds()), 60)
        # In theory we could end up with exactly 0 s, because of <=, but the chance is very low
        wait_str = f"{minutes} min {seconds} s" if minutes else f"{seconds} s"
        flash(
            f"Please wait {wait_str} before requesting another confirmation email.",
            "error",
        )
        return redirect(url_for("views.account"))

    activation_token = secrets.token_bytes(32)
    confirmation_url = url_for(
        ".confirm_email",
        _scheme="https",
        _external=True,
        token_enc=base64.urlsafe_b64encode(activation_token),
    )
    if saved_token:
        saved_token.token = activation_token
        saved_token.created_on = now
    else:
        saved_token = EmailToken(
            token=activation_token,
            token_type=TokenType.mail_confirmation,
            user_id=current_user.id,
        )
        db.session.add(saved_token)

    if production:
        send_confirmation_mail(
            current_user.username, current_user.email, confirmation_url
        )
    else:
        print(confirmation_url)
    db.session.commit()
    flash("An email with a confirmation link was sent.")
    return redirect(url_for("views.account"))

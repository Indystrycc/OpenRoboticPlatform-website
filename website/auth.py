import base64
import math
import re
import secrets
import sys
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from email.headerregistry import Address as EmailAddress
from typing import Any, TypeGuard

import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue
from flask_login import AnonymousUserMixin, login_required, login_user, logout_user
from markupsafe import Markup
from MySQLdb.constants.ER import DUP_ENTRY
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from . import csp_captcha, db, production, talisman
from .mailer import send_confirmation_mail, send_password_reset_mail
from .models import EmailToken, TokenType, User
from .secrets_manager import *
from .session_utils import get_session, get_user

USERNAME_PATTERN = re.compile(r"[\w]+", flags=re.ASCII)

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login() -> ResponseReturnValue:
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password", "")

        user = db.session.scalar(select(User).where(User.email == email))
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password", category="error")
        else:
            flash("No user registered with this email", category="error")
    return render_template("login.html")


@auth.route("logout")
@login_required
def logout() -> ResponseReturnValue:
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
@talisman(content_security_policy=csp_captcha)
def sign_up() -> ResponseReturnValue:
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")

        if check_captcha("signup"):
            user = db.session.scalar(select(User).where(User.email == email))
            if user:
                flash("This email is already registered.", category="error")
            elif username is None or len(username) < 4:
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
            elif not check_password_rules(password):
                # check_password_rules uses flash to show the errors
                pass
            elif not email:
                flash("Email is required", category="error")
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
                    db.session.flush()
                    activation_token = secrets.token_bytes(32)
                    confirmation_url = url_for(
                        ".confirm_email",
                        _scheme="https",
                        _external=True,
                        token_enc=base64.urlsafe_b64encode(activation_token).decode(
                            "ascii"
                        ),
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
                    if e.orig and e.orig.args[0] == DUP_ENTRY:
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
    return render_template("signup.html", recaptcha_site_key=RECAPTCHA_PUBLIC_KEY)


@auth.route("/signup/confirm/<token_enc>")
def confirm_email(token_enc: str) -> ResponseReturnValue:
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
        current_user = get_session()
        if isinstance(current_user, AnonymousUserMixin) or not current_user.confirmed:
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


@auth.route("/signup/resend-mail", methods=["POST"])
@login_required
def resend_confirmation_email() -> ResponseReturnValue:
    current_user = get_user()
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
        (saved_token.created_on + timedelta(minutes=5)) if saved_token else None
    )
    now = datetime.now(UTC)
    if allowed_after and now <= allowed_after:
        # In theory we could end up with exactly 0 s, because of <=, but the chance is very low
        wait = allowed_after - now
        wait_str = format_time_interval(wait)
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
        token_enc=base64.urlsafe_b64encode(activation_token).decode("ascii"),
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

    send_confirmation_mail(current_user.username, current_user.email, confirmation_url)
    db.session.commit()
    flash("An email with a confirmation link was sent.")
    return redirect(url_for("views.account"))


@auth.route("/reset-password", methods=["GET", "POST"])
@talisman(content_security_policy=csp_captcha)
def forgot_password() -> ResponseReturnValue:
    if request.method == "POST":
        email = request.form.get("email")

        if check_captcha("forgot_password"):
            user = db.session.scalar(select(User).where(User.email == email))
            if user:
                now = datetime.now(UTC)
                saved_token = db.session.scalar(
                    select(EmailToken)
                    .where(
                        EmailToken.user_id == user.id,
                        EmailToken.token_type == TokenType.password_reset,
                    )
                    .order_by(EmailToken.created_on.desc())
                )
                created_on = (
                    saved_token.created_on if saved_token else datetime.min
                ).replace(tzinfo=UTC)
                resend_if_after = created_on + timedelta(minutes=1)
                if now < resend_if_after:
                    wait = resend_if_after - now
                    wait_str = format_time_interval(wait)
                    flash(
                        f"Please wait {wait_str} before requesting another password reset email.",
                        "error",
                    )
                    return render_template(
                        "forgot-password.html",
                        recaptcha_site_key=RECAPTCHA_PUBLIC_KEY,
                    )

                else:
                    if saved_token:
                        db.session.delete(saved_token)
                    activation_token = secrets.token_bytes(32)
                    reset_url = url_for(
                        ".reset_password_token",
                        _scheme="https",
                        _external=True,
                        token_enc=base64.urlsafe_b64encode(activation_token).decode(
                            "ascii"
                        ),
                    )
                    saved_token = EmailToken(
                        token=activation_token,
                        token_type=TokenType.password_reset,
                        user_id=user.id,
                    )
                    db.session.add(saved_token)
                    send_password_reset_mail(user.username, user.email, reset_url)
                    db.session.commit()

            flash(
                f"Password reset link was sent to {email}. The link is valid for 15 minutes."
            )
        else:
            flash("CAPTCHA validation failed. Please try again.", category="error")

    return render_template(
        "forgot-password.html",
        recaptcha_site_key=RECAPTCHA_PUBLIC_KEY,
    )


@auth.route("/reset-password/<token_enc>", methods=["GET", "POST"])
@talisman(content_security_policy=csp_captcha)
def reset_password_token(token_enc: str) -> ResponseReturnValue:
    token = base64.urlsafe_b64decode(token_enc)
    valid_time = datetime.now(UTC) - timedelta(minutes=15)
    matching_token = db.session.scalar(
        select(EmailToken).where(
            EmailToken.token == token,
            EmailToken.token_type == TokenType.password_reset,
            EmailToken.created_on >= valid_time,
        )
    )
    if not matching_token:
        flash("Invalid or expired link.", "error")
        return redirect("/")

    user = matching_token.user
    if request.method == "POST":
        password = request.form.get("password")

        if check_password_rules(password):
            if check_captcha("reset_password"):
                user.password = generate_password_hash(
                    password, method="scrypt:131072:8:1"
                )
                db.session.delete(matching_token)
                db.session.commit()
                flash("You can now log in using the new password")
                return redirect("/login")
            else:
                flash("CAPTCHA validation failed. Please try again.", category="error")

    address = EmailAddress(addr_spec=user.email)
    uname = address.username
    uname_len = len(uname)
    username = (
        (uname[0] + "*" * (uname_len - 2) + uname[-1])
        if uname_len > 2
        else uname[0] + "*" * (uname_len - 1)
    )
    address = EmailAddress(username=username, domain=address.domain)
    return render_template(
        "reset-password.html",
        recaptcha_site_key=RECAPTCHA_PUBLIC_KEY,
        mail_addr=address,
    )


def format_time_interval(wait: timedelta) -> str:
    minutes, seconds = divmod(math.ceil(wait.total_seconds()), 60)
    wait_str = f"{minutes} min {seconds} s" if minutes else f"{seconds} s"
    return wait_str


def verify_recaptcha() -> "CaptchaV3Result":
    recaptcha_response = request.form.get("g-recaptcha-response")
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {"secret": RECAPTCHA_PRIVATE_KEY, "response": recaptcha_response}
    response = requests.post(url, data=data)
    return CaptchaV3Result(response.json())


def check_captcha(action: str, threshold: float = 0.5) -> bool:
    captcha_result = verify_recaptcha()
    print(captcha_result)
    return captcha_result.success and (
        not production
        or (captcha_result.score >= threshold and captcha_result.action == action)
    )


def check_password_rules(password: str | None) -> TypeGuard[str]:
    if password is None or len(password) < 8:
        flash("Password must be at least 8 characters long.", category="error")
        return False
    if len(password.encode("utf-8")) > 128:
        flash("Password must not be longer than 128 bytes.", category="error")
        return False
    return True


@dataclass
class CaptchaV3Result:
    success: bool
    challenge_ts: datetime
    hostname: str
    score: float
    action: str

    def __init__(self, data: Any) -> None:
        assert isinstance(data, dict)
        success = data["success"]
        challenge_ts = data["challenge_ts"]
        hostname = data["hostname"]
        score = data["score"]
        action = data["action"]

        correct = (
            isinstance(success, bool)
            and isinstance(challenge_ts, str)
            and isinstance(hostname, str)
            and isinstance(score, float)
            and isinstance(action, str)
        )
        if not correct:
            print("Invalid captcha data", data)
            self.success = False
            self.challenge_ts = datetime.min
            self.hostname = ""
            self.score = 0.0
            self.action = ""
        else:
            self.success = success
            self.challenge_ts = datetime.fromisoformat(challenge_ts)
            self.hostname = hostname
            self.score = score
            self.action = action

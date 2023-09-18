from flask import abort
from flask_login import AnonymousUserMixin, current_user

from . import login_manager
from .models import User


def get_session() -> User | AnonymousUserMixin:
    """
    Returns the current_user extracted from its LocalProxy whether
    the user is logged in (`User`) or not (`AnonymousUserMixin`).
    """
    return current_user._get_current_object()  # type: ignore


def get_user() -> User:
    """
    Returns the logged in `User`. If the user is not logged in the request processing will be aborted and
    the user will be redirected to the login page (`login_manager.unauthorized()`) as if the route was
    decorated with `@login_required`.

    Please use `@login_required` if you want to call `get_user()` to explicitly mark the route as requiring
    authenticated sessions.
    """
    user = get_session()
    if not user.is_authenticated or not isinstance(user, User):
        abort(login_manager.unauthorized())

    return user

from datetime import timedelta
from typing import Any, Callable, Generic, Literal, NoReturn, TypeVar

from flask import Flask, Response
from flask.typing import BeforeRequestCallable, RouteCallable
from werkzeug.local import LocalProxy

class UserMixin:
    """
    This provides default implementations for the methods that Flask-Login
    expects user objects to have.
    """

    @property
    def is_active(self) -> Literal[True]: ...
    @property
    def is_authenticated(self) -> Literal[True]: ...
    @property
    def is_anonymous(self) -> Literal[False]: ...
    def get_id(self) -> str: ...

class AnonymousUserMixin:
    """
    This is the default object for representing an anonymous user.
    """

    @property
    def is_authenticated(self) -> Literal[False]: ...
    @property
    def is_active(self) -> Literal[False]: ...
    @property
    def is_anonymous(self) -> Literal[True]: ...
    def get_id(self) -> None: ...

_FL_USER = TypeVar("_FL_USER", bound=UserMixin)

class LoginManager(Generic[_FL_USER]):
    """This object is used to hold the settings used for logging in. Instances
    of :class:`LoginManager` are *not* bound to specific apps, so you can
    create one in the main body of your code and then bind it to your
    app in a factory function.
    """

    anonymous_user = AnonymousUserMixin
    login_view: str | None
    login_message: str
    login_message_category: str
    refresh_view: str | None
    needs_refresh_message: str
    needs_refresh_message_category: str
    session_protection: Literal["basic"] | Literal["strong"] | None = "basic"
    def __init__(
        self, app: Flask | None = None, add_context_processor: bool = True
    ) -> None: ...
    def init_app(self, app: Flask, add_context_processor: bool = True) -> None: ...
    def unauthorized(self) -> Any | Response | NoReturn: ...
    def user_loader(
        self, callback: Callable[[str], _FL_USER | None]
    ) -> Callable[[str], _FL_USER | None] | None: ...
    @property
    def user_callback(self) -> Callable[[str], _FL_USER | None] | None: ...
    def needs_refresh(self) -> Any | Response | NoReturn: ...

_FL_CALLABLE_ROUTE = TypeVar(
    "_FL_CALLABLE_ROUTE", bound=RouteCallable | BeforeRequestCallable
)

current_user: LocalProxy[UserMixin | AnonymousUserMixin]

def login_fresh() -> bool: ...
def login_remembered() -> bool: ...
def login_user(
    user: UserMixin,
    remember: bool = False,
    duration: timedelta | None = None,
    force: bool = False,
    fresh: bool = False,
) -> bool: ...
def logout_user() -> None: ...
def confirm_login() -> None: ...
def login_required(func: _FL_CALLABLE_ROUTE) -> _FL_CALLABLE_ROUTE: ...
def fresh_login_required(func: _FL_CALLABLE_ROUTE) -> _FL_CALLABLE_ROUTE: ...
def login_url(
    login_view: str, next_url: str | None = None, next_field: str = "next"
) -> str: ...

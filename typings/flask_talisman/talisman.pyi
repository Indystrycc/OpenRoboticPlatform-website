from typing import Callable, Literal, Mapping, Sequence, TypedDict, Unpack

from flask import Flask
from flask.typing import RouteCallable

DENY: Literal["DENY"] = "DENY"
SAMEORIGIN: Literal["SAMEORIGIN"] = "SAMEORIGIN"
ALLOW_FROM: Literal["ALLOW-FROM"] = "ALLOW-FROM"
ONE_YEAR_IN_SECS: Literal[31556926] = 31556926
DEFAULT_REFERRER_POLICY: Literal["strict-origin-when-cross-origin"] = (
    "strict-origin-when-cross-origin"
)
DEFAULT_CSP_POLICY = {
    "default-src": "'self'",
    "object-src": "'none'",
}
DEFAULT_SESSION_COOKIE_SAMESITE: Literal["Lax"] = "Lax"
GOOGLE_CSP_POLICY = {
    # Fonts from fonts.google.com
    "font-src": "'self' themes.googleusercontent.com *.gstatic.com",
    # <iframe> based embedding for Maps and Youtube.
    "frame-src": "'self' www.google.com www.youtube.com",
    # Assorted Google-hosted Libraries/APIs.
    "script-src": "'self' ajax.googleapis.com *.googleanalytics.com "
    "*.google-analytics.com",
    # Used by generated code from http://www.google.com/fonts
    "style-src": "'self' ajax.googleapis.com fonts.googleapis.com " "*.gstatic.com",
    "object-src": "'none'",
    "default-src": "'self' *.gstatic.com",
}
DEFAULT_PERMISSIONS_POLICY = {
    # Disable Topics API
    "browsing-topics": "()"
}
DEFAULT_DOCUMENT_POLICY: dict[str, str] = {}
DEFAULT_FEATURE_POLICY: dict[str, str] = {}
NONCE_LENGTH = 32

class TalismanViewOptions(TypedDict, total=False):
    feature_policy: dict[str, str] | str
    permissions_policy: dict[str, str] | str
    document_policy: dict[str, str] | str
    force_https: bool
    frame_options: Literal["SAMEORIGIN", "DENY", "ALLOWFROM"]
    frame_options_allow_from: str | None
    content_security_policy: Mapping[str, str | Sequence[str]] | str
    content_security_policy_nonce_in: Sequence[str]

class TalismanAppOptions(TalismanViewOptions, total=False):
    force_https_permanent: bool
    force_file_save: bool
    strict_transport_security: bool
    strict_transport_security_preload: bool
    strict_transport_security_max_age: int
    strict_transport_security_include_subdomains: bool
    content_security_policy_report_uri: str | None
    content_security_policy_report_only: bool
    referrer_policy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]
    session_cookie_secure: bool
    session_cookie_http_only: bool
    session_cookie_samesite: Literal["Strict", "Lax", "None"]
    x_content_type_options: bool
    x_xss_protection: bool

class Talisman:
    def __init__(
        self, app: Flask | None = None, **kwargs: Unpack[TalismanAppOptions]
    ) -> None: ...
    feature_policy: dict[str, str] | str
    permissions_policy: dict[str, str] | str
    document_policy: dict[str, str] | str
    force_https: bool
    force_https_permanent: bool
    frame_options: Literal["SAMEORIGIN", "DENY", "ALLOWFROM"]
    frame_options_allow_from: str | None
    strict_transport_security: bool
    strict_transport_security_preload: bool
    strict_transport_security_max_age: int
    strict_transport_security_include_subdomains: bool
    content_security_policy: Mapping[str, str | Sequence[str]] | str
    content_security_policy_report_uri: str | None
    content_security_policy_report_only: bool
    content_security_policy_nonce_in: Sequence[str] | None
    referrer_policy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]
    session_cookie_secure: bool
    force_file_save: bool
    x_content_type_options: bool
    x_xss_protection: bool
    app: Flask
    def init_app(
        self,
        app: Flask,
        feature_policy: dict[str, str] | str = DEFAULT_FEATURE_POLICY,
        permissions_policy: dict[str, str] | str = DEFAULT_PERMISSIONS_POLICY,
        document_policy: dict[str, str] | str = DEFAULT_DOCUMENT_POLICY,
        force_https: bool = True,
        force_https_permanent: bool = False,
        force_file_save: bool = False,
        frame_options: Literal["SAMEORIGIN", "DENY", "ALLOWFROM"] = SAMEORIGIN,
        frame_options_allow_from: str | None = None,
        strict_transport_security: bool = True,
        strict_transport_security_preload: bool = False,
        strict_transport_security_max_age: int = ONE_YEAR_IN_SECS,
        strict_transport_security_include_subdomains: bool = True,
        content_security_policy: (
            Mapping[str, str | Sequence[str]] | str
        ) = DEFAULT_CSP_POLICY,
        content_security_policy_report_uri: str | None = None,
        content_security_policy_report_only: bool = False,
        content_security_policy_nonce_in: Sequence[str] | None = [],
        referrer_policy: Literal[
            "no-referrer",
            "no-referrer-when-downgrade",
            "origin",
            "origin-when-cross-origin",
            "same-origin",
            "strict-origin",
            "strict-origin-when-cross-origin",
            "unsafe-url",
        ] = DEFAULT_REFERRER_POLICY,
        session_cookie_secure: bool = True,
        session_cookie_http_only: bool = True,
        session_cookie_samesite: Literal[
            "Strict", "Lax", "None"
        ] = DEFAULT_SESSION_COOKIE_SAMESITE,
        x_content_type_options: bool = True,
        x_xss_protection: bool = False,
    ) -> None: ...
    def __call__(
        self, **kwargs: Unpack[TalismanViewOptions]
    ) -> Callable[[RouteCallable], RouteCallable]: ...

def get_random_string(length: int) -> str: ...

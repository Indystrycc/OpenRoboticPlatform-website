import sys
from os import environ

_ok = False
if "SECRETS_FILE" in environ.keys():
    import importlib.util

    try:
        spec = importlib.util.spec_from_file_location(
            "secret", environ.get("SECRETS_FILE")
        )
        assert spec and spec.loader
        secret_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(secret_module)

        SECRET_KEY: str = secret_module.SECRET_KEY
        RECAPTCHA_PUBLIC_KEY: str = secret_module.RECAPTCHA_PUBLIC_KEY
        RECAPTCHA_PRIVATE_KEY: str = secret_module.RECAPTCHA_PRIVATE_KEY
        MAILERLITE_API_KEY: str = secret_module.MAILERLITE_API_KEY
        _ok = True
    except Exception as e:
        print(
            f"Could not import secrets from {environ.get('SECRETS_FILE')}",
            file=sys.stderr,
        )
        print(e, file=sys.stderr)

if _ok:
    pass
elif set(
    (
        "SECRET_KEY",
        "RECAPTCHA_PUBLIC_KEY",
        "RECAPTCHA_PRIVATE_KEY",
        "MAILERLITE_API_KEY",
    )
).issubset(environ.keys()):
    SECRET_KEY = environ.get("SECRET_KEY", "")
    RECAPTCHA_PUBLIC_KEY = environ.get("RECAPTCHA_PUBLIC_KEY", "")
    RECAPTCHA_PRIVATE_KEY = environ.get("RECAPTCHA_PRIVATE_KEY", "")
    MAILERLITE_API_KEY = environ.get("MAILERLITE_API_KEY", "")

else:
    try:
        from .secret import (
            MAILERLITE_API_KEY,
            RECAPTCHA_PRIVATE_KEY,
            RECAPTCHA_PUBLIC_KEY,
            SECRET_KEY,
        )
    except ImportError:
        from sys import stderr

        print(
            """Please configure secrets using one of the following methods:
1. SECRETS_FILE environmental variable pointing to a Python file exposing constants SECRET_KEY, RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY and MAILERLITE_API_KEY
2. SECRET_KEY, RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY and MAILERLITE_API_KEY environmental variables
3. website/secret.py file with the same content as in 1.""",
            file=stderr,
        )
        exit(1)

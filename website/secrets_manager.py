from os import environ

if "SECRETS_FILE" in environ.keys():
    import importlib.util

    spec = importlib.util.spec_from_file_location("secret", environ.get("SECRETS_FILE"))
    secret_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(secret_module)

    SECRET_KEY: str = secret_module.SECRET_KEY
    RECAPTCHA_PUBLIC_KEY: str = secret_module.RECAPTCHA_PUBLIC_KEY
    RECAPTCHA_PRIVATE_KEY: str = secret_module.RECAPTCHA_PRIVATE_KEY

elif set(("SECRET_KEY", "RECAPTCHA_PUBLIC_KEY", "RECAPTCHA_PRIVATE_KEY")).issubset(
    environ.keys()
):
    SECRET_KEY = environ.get("SECRET_KEY")
    RECAPTCHA_PUBLIC_KEY = environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = environ.get("RECAPTCHA_PRIVATE_KEY")

else:
    try:
        from .secret import SECRET_KEY, RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY
    except ImportError:
        from sys import stderr

        print(
            """Please configure secrets using one of the following methods:
1. SECRETS_FILE environmental variable pointing to a Python file exposing constants SECRET_KEY, RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY
2. SECRET_KEY, RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY environmental variables
3. website/secret.py file with the same content as in 1.""",
            file=stderr,
        )
        exit(1)

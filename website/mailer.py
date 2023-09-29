import ipaddress
import textwrap
from email.headerregistry import Address
from email.message import EmailMessage, MIMEPart
from os import getenv
from smtplib import SMTP

from . import production

FROM_ADDR = Address(
    getenv("MAIL_FULL_NAME", "OpenRoboticPlatform"),
    getenv("MAIL_USER", "noreply"),
    getenv("MAIL_DOMAIN", "orp.testing"),
)


def check_addr_restrictions(address: Address) -> None:
    domain = address.domain.lower()
    if domain.startswith("["):
        ip = ipaddress.ip_address(
            domain[6:-1] if domain.startswith("[ipv6:") else domain[1:-1]
        )
        if (
            not ip.is_global
            or ip.is_link_local
            or ip.is_loopback
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            # There are ways around this check, but let's do it anyway
            raise ValueError("Mail uses a forbidden IP address")
    elif "." not in domain:
        raise ValueError("Mail is registered under a TLD")


def send_message(msg: EmailMessage) -> None:
    if production:
        with SMTP("postfix") as smtp:
            smtp.send_message(msg)
    else:
        print(f'To: {msg["To"]}')
        print(f'From: {msg["From"]}')
        print(f'Subject: {msg["Subject"]}\n')
        body = msg.get_body(("plain", "html"))
        if isinstance(body, MIMEPart):
            print(body.get_content())


def send_confirmation_mail(username: str, email_addr: str, url: str) -> None:
    addr = Address(username, addr_spec=email_addr)
    check_addr_restrictions(addr)
    msg = EmailMessage()
    msg["Subject"] = "Confirm your email address"
    msg["From"] = FROM_ADDR
    msg["To"] = addr
    msg.set_content(
        textwrap.dedent(
            f"""\
            Hello!

            Thank you for creating an OpenRoboticPlatform account. Before uploading your
            first part you have to confirm your email address using the link below:

            {url}

            If you did not create an OpenRoboticPlatform account please ignore this message.

            Regards,
            OpenRoboticPlatform Team
            """
        )
    )
    msg.add_alternative(
        textwrap.dedent(
            f"""\
            <html>
                <body>
                    <p>Hello!</p>
                    <p>
                        Thank you for creating an OpenRoboticPlatform account. Before uploading your
                        first part you have to confirm your email address using the link below:
                    </p>
                    <p><a href="{url}">{url}</a></p>
                    <p>If you did not create an OpenRoboticPlatform account please ignore this message.</p>
                    <p>
                        Regards,<br>
                        OpenRoboticPlatform Team
                    </p>
                </body>
            </html>
            """
        ),
        subtype="html",
    )

    send_message(msg)


def send_password_reset_mail(username: str, email_addr: str, url: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = "Password reset link"
    msg["From"] = FROM_ADDR
    msg["To"] = Address(username, addr_spec=email_addr)
    msg.set_content(
        textwrap.dedent(
            f"""\
            Hello!

            To reset your password use the link below. The link is valid for 15 minutes.

            {url}

            If you did not request a password reset link please ignore this message.

            Regards,
            OpenRoboticPlatform Team
            """
        )
    )
    msg.add_alternative(
        textwrap.dedent(
            f"""\
            <html>
                <body>
                    <p>Hello!</p>
                    <p>
                        To reset your password use the link below. The link is valid for 15 minutes.
                    </p>
                    <p><a href="{url}">{url}</a></p>
                    <p>If you did not request a password reset link please ignore this message.</p>
                    <p>
                        Regards,<br>
                        OpenRoboticPlatform Team
                    </p>
                </body>
            </html>
            """
        ),
        subtype="html",
    )

    send_message(msg)

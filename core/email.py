import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import settings

logger = logging.getLogger(__name__)


class EmailDeliveryError(Exception):
    pass


def _is_email_configured() -> bool:
    return bool(
        settings.EMAIL_ENABLED
        and settings.SMTP_HOST
        and settings.SMTP_USER
        and settings.SMTP_PASSWORD
        and settings.SMTP_FROM_EMAIL
    )


def send_email(
    *,
    to_email: str,
    subject: str,
    text_content: str,
    html_content: str | None = None,
) -> None:
    if not _is_email_configured():
        logger.error(
            "Email not configured: EMAIL_ENABLED=%s SMTP_HOST=%r SMTP_USER=%s",
            settings.EMAIL_ENABLED,
            settings.SMTP_HOST,
            bool(settings.SMTP_USER),
        )
        raise EmailDeliveryError("Email service is not configured")

    sender = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email
    msg.attach(MIMEText(text_content, "plain"))
    if html_content:
        msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(sender, to_email, msg.as_string())
        logger.info("Email sent to=%r subject=%r", to_email, subject)

    except Exception as exc:
        logger.error(
            "Failed to send email to=%r: %s: %s",
            to_email,
            type(exc).__name__,
            exc,
            exc_info=True,
        )
        raise EmailDeliveryError("Failed to send email") from exc

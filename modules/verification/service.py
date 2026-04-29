import logging
from datetime import datetime, timedelta
from secrets import randbelow

from sqlmodel import Session, select

from core.config import settings
from core.email import EmailDeliveryError, send_email
from core.email_templates import password_reset_html, verification_code_html
from core.security import hash_password
from modules.users.models import User

from .models import PasswordResetCode, VerificationCode

logger = logging.getLogger(__name__)

VERIFICATION_CODE_TTL_MINUTES = 15
MAX_VERIFICATION_ATTEMPTS = 5
RESET_CODE_TTL_MINUTES = 60


class VerificationError(Exception):
    pass


class UserNotFoundError(VerificationError):
    pass


class AlreadyVerifiedError(VerificationError):
    pass


class VerificationCodeNotFoundError(VerificationError):
    pass


class VerificationCodeExpiredError(VerificationError):
    pass


class InvalidVerificationCodeError(VerificationError):
    pass


class VerificationEmailDeliveryError(VerificationError):
    pass


class PasswordResetCodeNotFoundError(VerificationError):
    pass


class PasswordResetCodeExpiredError(VerificationError):
    pass


class InvalidPasswordResetCodeError(VerificationError):
    pass


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _generate_code(length: int = 6) -> str:
    return "".join(str(randbelow(10)) for _ in range(length))


def _get_user_by_email(db: Session, email: str) -> User | None:
    return db.exec(select(User).where(User.email == _normalize_email(email))).first()


def _get_active_code(db: Session, user_id: int) -> VerificationCode | None:
    return db.exec(
        select(VerificationCode)
        .where(
            VerificationCode.user_id == user_id,
            VerificationCode.is_active.is_(True),
            VerificationCode.used_at.is_(None),
        )
        .order_by(VerificationCode.created_at.desc())
    ).first()


def _verification_email_subject() -> str:
    return f"{settings.PROJECT_NAME} - Verification code"


def _verification_email_text(user: User, code: str) -> str:
    return (
        f"Hola {user.name},\n\n"
        f"Tu codigo de verificacion es: {code}\n"
        f"Este codigo expira en {VERIFICATION_CODE_TTL_MINUTES} minutos.\n\n"
        "Si no solicitaste este codigo, ignora este correo."
    )


def _verification_email_html(user: User, code: str) -> str:
    return verification_code_html(user.name, code, VERIFICATION_CODE_TTL_MINUTES)


def _send_verification_email(user: User, code: str) -> None:
    if not settings.EMAIL_ENABLED:
        if settings.DEBUG:
            logger.debug(
                "EMAIL_ENABLED=False — skipping send. user_id=%s email=%r code=%s",
                user.id,
                user.email,
                code,
            )
            return
        logger.warning(
            "Email service disabled (EMAIL_ENABLED=False) — verification email not sent. user_id=%s",
            user.id,
        )
        raise VerificationEmailDeliveryError("Email service is disabled")

    logger.debug("Sending verification email: user_id=%s email=%r", user.id, user.email)
    try:
        send_email(
            to_email=user.email,
            subject=_verification_email_subject(),
            text_content=_verification_email_text(user, code),
            html_content=_verification_email_html(user, code),
        )
        logger.info("Verification email sent: user_id=%s email=%r", user.id, user.email)
    except EmailDeliveryError as exc:
        logger.error(
            "Failed to send verification email: user_id=%s email=%r — %s",
            user.id,
            user.email,
            exc,
            exc_info=True,
        )
        raise VerificationEmailDeliveryError("Failed to send verification email") from exc


def create_verification_code(db: Session, user: User) -> VerificationCode:
    now = datetime.now()
    active_codes = list(
        db.exec(
            select(VerificationCode).where(
                VerificationCode.user_id == user.id,
                VerificationCode.is_active.is_(True),
            )
        )
    )
    resend_count = 0
    if active_codes:
        resend_count = max(code.resended_count for code in active_codes) + 1
        for code in active_codes:
            code.is_active = False
            code.updated_at = now
            db.add(code)

    verification_code = VerificationCode(
        code=_generate_code(),
        user_id=user.id,
        resended_count=resend_count,
        expired_at=now + timedelta(minutes=VERIFICATION_CODE_TTL_MINUTES),
        created_at=now,
        updated_at=now,
    )
    db.add(verification_code)
    db.commit()
    db.refresh(verification_code)
    return verification_code


def create_and_send_verification_code(db: Session, user: User) -> VerificationCode:
    verification_code = create_verification_code(db, user)
    _send_verification_email(user, verification_code.code)
    return verification_code


def request_email_verification(db: Session, email: str) -> VerificationCode:
    user = _get_user_by_email(db, email)
    if user is None:
        raise UserNotFoundError("User not found")
    if user.is_verified:
        raise AlreadyVerifiedError("Account already verified")
    return create_and_send_verification_code(db, user)


def confirm_email_verification(db: Session, email: str, code: str) -> User:
    user = _get_user_by_email(db, email)
    if user is None:
        raise UserNotFoundError("User not found")
    if user.is_verified:
        return user

    verification_code = _get_active_code(db, user.id)
    if verification_code is None:
        raise VerificationCodeNotFoundError("No active verification code")

    now = datetime.now()
    if verification_code.expired_at <= now:
        verification_code.is_active = False
        verification_code.updated_at = now
        db.add(verification_code)
        db.commit()
        raise VerificationCodeExpiredError("Verification code has expired")

    if verification_code.code != code.strip():
        verification_code.attemp_count += 1
        if verification_code.attemp_count >= MAX_VERIFICATION_ATTEMPTS:
            verification_code.is_active = False
        verification_code.updated_at = now
        db.add(verification_code)
        db.commit()
        raise InvalidVerificationCodeError("Invalid verification code")

    verification_code.used_at = now
    verification_code.is_active = False
    verification_code.updated_at = now
    user.is_verified = True
    user.updated_at = now

    db.add(verification_code)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _reset_email_subject() -> str:
    return f"{settings.PROJECT_NAME} - Restablecimiento de contraseña"


def _reset_email_text(user: User, code: str) -> str:
    return (
        f"Hola {user.name},\n\n"
        f"Tu codigo de restablecimiento es: {code}\n"
        f"Este codigo expira en {RESET_CODE_TTL_MINUTES} minutos.\n\n"
        "Si no solicitaste este cambio, ignora este correo."
    )


def _send_reset_email(user: User, code: str) -> None:
    if not settings.EMAIL_ENABLED:
        if settings.DEBUG:
            logger.debug(
                "EMAIL_ENABLED=False — skipping reset email. user_id=%s email=%r code=%s",
                user.id,
                user.email,
                code,
            )
            return
        logger.warning(
            "Email service disabled — reset email not sent. user_id=%s",
            user.id,
        )
        raise VerificationEmailDeliveryError("Email service is disabled")

    logger.debug("Sending reset email: user_id=%s email=%r", user.id, user.email)
    try:
        send_email(
            to_email=user.email,
            subject=_reset_email_subject(),
            text_content=_reset_email_text(user, code),
            html_content=password_reset_html(user.name, code, RESET_CODE_TTL_MINUTES),
        )
        logger.info("Reset email sent: user_id=%s email=%r", user.id, user.email)
    except EmailDeliveryError as exc:
        logger.error(
            "Failed to send reset email: user_id=%s email=%r — %s",
            user.id,
            user.email,
            exc,
            exc_info=True,
        )
        raise VerificationEmailDeliveryError("Failed to send reset email") from exc


def _get_latest_unused_reset_code(db: Session, user_id: int) -> PasswordResetCode | None:
    return db.exec(
        select(PasswordResetCode)
        .where(
            PasswordResetCode.user_id == user_id,
            PasswordResetCode.used_at.is_(None),
        )
        .order_by(PasswordResetCode.created_at.desc())
    ).first()


def create_password_reset_code(db: Session, user: User) -> PasswordResetCode:
    now = datetime.now()
    # Mark all existing unused codes as used (superseded by new request)
    existing = list(
        db.exec(
            select(PasswordResetCode).where(
                PasswordResetCode.user_id == user.id,
                PasswordResetCode.used_at.is_(None),
            )
        )
    )
    for old_code in existing:
        old_code.used_at = now
        old_code.updated_at = now
        db.add(old_code)

    reset_code = PasswordResetCode(
        code=_generate_code(),
        user_id=user.id,
        expired_at=now + timedelta(minutes=RESET_CODE_TTL_MINUTES),
        created_at=now,
        updated_at=now,
    )
    db.add(reset_code)
    db.commit()
    db.refresh(reset_code)
    return reset_code


def request_password_reset(db: Session, email: str) -> PasswordResetCode:
    user = _get_user_by_email(db, email)
    if user is None:
        raise UserNotFoundError("User not found")
    reset_code = create_password_reset_code(db, user)
    _send_reset_email(user, reset_code.code)
    return reset_code


def confirm_password_reset(db: Session, email: str, code: str, new_password: str) -> None:
    user = _get_user_by_email(db, email)
    if user is None:
        raise UserNotFoundError("User not found")

    reset_code = _get_latest_unused_reset_code(db, user.id)
    if reset_code is None:
        raise PasswordResetCodeNotFoundError("No active reset code. Request a new one")

    now = datetime.now()
    if reset_code.expired_at <= now:
        raise PasswordResetCodeExpiredError("Reset code has expired. Request a new one")

    if reset_code.code != code.strip():
        raise InvalidPasswordResetCodeError("Invalid reset code")

    reset_code.used_at = now
    reset_code.updated_at = now
    user.password = hash_password(new_password)
    user.updated_at = now

    db.add(reset_code)
    db.add(user)
    db.commit()

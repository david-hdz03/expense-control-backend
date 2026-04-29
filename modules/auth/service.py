from dataclasses import dataclass
from datetime import datetime

from sqlmodel import Session, select

from core.config import settings
from core.security import create_access_token, create_refresh_token, hash_password, verify_password
from modules.users.models import User
from modules.verification import service as verification_service

from .schemas import Token, UserRegister

VerificationEmailDeliveryError = verification_service.VerificationEmailDeliveryError


@dataclass
class RegisterResult:
    user: User
    verification_code: str
    verification_expires_at: datetime


def _issue_tokens(user_id: int) -> Token:
    return Token(
        access_token=create_access_token(str(user_id), settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh_token=create_refresh_token(str(user_id), settings.REFRESH_TOKEN_EXPIRE_DAYS),
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def get_by_email(db: Session, email: str) -> User | None:
    return db.exec(select(User).where(User.email == email.strip().lower())).first()


def register(db: Session, payload: UserRegister) -> RegisterResult:
    user = User(
        name=payload.name,
        second_name=payload.second_name,
        paternal_last_name=payload.paternal_last_name,
        maternal_last_name=payload.maternal_last_name,
        email=payload.email.strip().lower(),
        password=hash_password(payload.password),
        age=payload.age,
        currency_code=payload.currency_code.upper(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    verification_code = verification_service.create_and_send_verification_code(db, user)
    return RegisterResult(
        user=user,
        verification_code=verification_code.code,
        verification_expires_at=verification_code.expired_at,
    )


def authenticate(db: Session, email: str, password: str) -> User | None:
    user = get_by_email(db, email)
    if user is None or not verify_password(password, user.password):
        return None
    return user


def issue_tokens(user_id: int) -> Token:
    return _issue_tokens(user_id)

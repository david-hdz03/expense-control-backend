from dataclasses import dataclass
from datetime import datetime

import requests as http_requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from sqlmodel import Session, select

from core.config import settings
from core.security import create_access_token, create_refresh_token, hash_password, verify_password
from modules.users.models import User
from modules.verification import service as verification_service

from .schemas import Token, UserRegister

VerificationEmailDeliveryError = verification_service.VerificationEmailDeliveryError


class GoogleTokenError(Exception):
    pass


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
    if user is None or user.password is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def _claims_from_id_token(id_token_str: str, allowed: list[str]) -> dict:
    try:
        claims = google_id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            audience=None,
        )
    except ValueError as exc:
        raise GoogleTokenError("Invalid Google id_token") from exc
    aud = claims.get("aud", "")
    aud_list = aud if isinstance(aud, list) else [aud]
    if not any(a in allowed for a in aud_list):
        raise GoogleTokenError("Token audience not recognized")
    return claims


def _claims_from_access_token(access_token_str: str) -> dict:
    try:
        resp = http_requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token_str}"},
            timeout=10,
        )
    except Exception as exc:
        raise GoogleTokenError("Failed to reach Google userinfo endpoint") from exc
    if resp.status_code != 200:
        raise GoogleTokenError(f"Google userinfo returned {resp.status_code}")
    return resp.json()


def google_authenticate(db: Session, id_token_str: str | None, access_token_str: str | None = None) -> Token:
    allowed = settings.google_allowed_client_ids
    if not allowed:
        raise GoogleTokenError("Google OAuth not configured")

    if id_token_str:
        claims = _claims_from_id_token(id_token_str, allowed)
    elif access_token_str:
        claims = _claims_from_access_token(access_token_str)
    else:
        raise GoogleTokenError("No token provided")

    email = claims.get("email", "").lower().strip()
    if not email:
        raise GoogleTokenError("Token missing email")
    if not claims.get("email_verified"):
        raise GoogleTokenError("Google email not verified")

    now = datetime.now()
    user = get_by_email(db, email)
    if user is None:
        raw_name = claims.get("given_name") or (claims.get("name") or "User")
        name = raw_name.split()[0] if " " in raw_name else raw_name
        paternal = claims.get("family_name") or name
        user = User(
            name=name,
            paternal_last_name=paternal,
            email=email,
            password=None,
            age=0,
            auth_provider="google",
            is_verified=True,
            currency_code="USD",
            created_at=now,
            updated_at=now,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        if not user.is_active:
            raise GoogleTokenError("Account is disabled")
        if not user.is_verified:
            user.is_verified = True
            user.updated_at = now
            db.add(user)
            db.commit()

    return _issue_tokens(user.id)


def issue_tokens(user_id: int) -> Token:
    return _issue_tokens(user_id)

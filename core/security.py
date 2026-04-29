from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from core.config import settings

_ACCESS_TOKEN_TYPE = "access"
_REFRESH_TOKEN_TYPE = "refresh"
_BCRYPT_MAX_BYTES = 72


class TokenError(Exception):
    pass


class InvalidTokenError(TokenError):
    pass


class ExpiredTokenError(TokenError):
    pass


def _encode_for_bcrypt(plain: str) -> bytes:
    return plain.encode("utf-8")[:_BCRYPT_MAX_BYTES]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_encode_for_bcrypt(password), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str | None) -> bool:
    if not hashed:
        return False
    try:
        return bcrypt.checkpw(_encode_for_bcrypt(password), hashed.encode())
    except (ValueError, AttributeError):
        return False


def _create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + expires_delta,
        "type": token_type,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def create_access_token(subject: str, expires_minutes: int = 15) -> str:
    return _create_token(subject, _ACCESS_TOKEN_TYPE, timedelta(minutes=expires_minutes))


def create_refresh_token(subject: str, expires_days: int = 7) -> str:
    return _create_token(subject, _REFRESH_TOKEN_TYPE, timedelta(days=expires_days))


def decode_token(token: str, expected_type: str) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError as exc:
        raise ExpiredTokenError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise InvalidTokenError("Invalid token") from exc

    if payload.get("type") != expected_type:
        raise InvalidTokenError(f"Expected token type {expected_type!r}")
    return payload

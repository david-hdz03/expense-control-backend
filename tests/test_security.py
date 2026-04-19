from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.core import security
from app.core.config import settings


def test_hash_password_produces_different_output_each_time():
    hashed_a = security.hash_password("Str0ng!Password")
    hashed_b = security.hash_password("Str0ng!Password")
    assert hashed_a != "Str0ng!Password"
    assert hashed_a != hashed_b  # bcrypt salt


def test_verify_password_happy_path():
    hashed = security.hash_password("Str0ng!Password")
    assert security.verify_password("Str0ng!Password", hashed) is True


def test_verify_password_wrong_password_returns_false():
    hashed = security.hash_password("Str0ng!Password")
    assert security.verify_password("WrongPassword1!", hashed) is False


def test_access_token_roundtrip():
    token = security.create_access_token("42")
    payload = security.decode_token(token, expected_type="access")
    assert payload["sub"] == "42"
    assert payload["type"] == "access"
    assert "iat" in payload
    assert "exp" in payload


def test_refresh_token_roundtrip():
    token = security.create_refresh_token("42")
    payload = security.decode_token(token, expected_type="refresh")
    assert payload["sub"] == "42"
    assert payload["type"] == "refresh"


def test_access_token_decoded_as_refresh_raises_invalid():
    token = security.create_access_token("42")
    with pytest.raises(security.InvalidTokenError):
        security.decode_token(token, expected_type="refresh")


def test_refresh_token_decoded_as_access_raises_invalid():
    token = security.create_refresh_token("42")
    with pytest.raises(security.InvalidTokenError):
        security.decode_token(token, expected_type="access")


def test_expired_token_raises_expired_error():
    now = datetime.now(timezone.utc)
    payload = {
        "sub": "42",
        "iat": now - timedelta(hours=1),
        "exp": now - timedelta(minutes=1),
        "type": "access",
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    with pytest.raises(security.ExpiredTokenError):
        security.decode_token(token, expected_type="access")


def test_token_signed_with_wrong_secret_raises_invalid():
    now = datetime.now(timezone.utc)
    payload = {
        "sub": "42",
        "iat": now,
        "exp": now + timedelta(minutes=5),
        "type": "access",
    }
    token = jwt.encode(payload, "a-different-secret", algorithm=settings.jwt_algorithm)
    with pytest.raises(security.InvalidTokenError):
        security.decode_token(token, expected_type="access")


def test_malformed_token_raises_invalid():
    with pytest.raises(security.InvalidTokenError):
        security.decode_token("not-a-real-jwt", expected_type="access")


def test_access_token_extra_claims_are_embedded():
    token = security.create_access_token("42", extra_claims={"role": "admin"})
    payload = security.decode_token(token, expected_type="access")
    assert payload["role"] == "admin"
    assert payload["sub"] == "42"
    assert payload["type"] == "access"


def test_token_exceptions_inherit_from_token_error():
    assert issubclass(security.InvalidTokenError, security.TokenError)
    assert issubclass(security.ExpiredTokenError, security.TokenError)

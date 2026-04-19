import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate


def test_password_valid_passes():
    user = UserCreate(email="user@example.com", password="Str0ng!Pass")
    assert user.password == "Str0ng!Pass"


def test_password_too_short_rejected():
    with pytest.raises(ValidationError):
        UserCreate(email="user@example.com", password="Ab1!xyz")


def test_password_without_uppercase_rejected():
    with pytest.raises(ValidationError):
        UserCreate(email="user@example.com", password="str0ng!pass")


def test_password_without_digit_rejected():
    with pytest.raises(ValidationError):
        UserCreate(email="user@example.com", password="Strong!Pass")


def test_password_without_symbol_rejected():
    with pytest.raises(ValidationError):
        UserCreate(email="user@example.com", password="Str0ngPass")

import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class VerificationRequest(BaseModel):
    email: str


class VerificationRequestResponse(BaseModel):
    detail: str
    expires_at: datetime
    verification_code: str | None = None


class VerificationConfirm(BaseModel):
    email: str
    code: str = Field(..., min_length=6, max_length=6)

    @field_validator("code")
    @classmethod
    def _only_digits(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Verification code must contain only digits")
        return v


class VerificationConfirmResponse(BaseModel):
    detail: str
    verified: bool = True


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetRequestResponse(BaseModel):
    detail: str
    expires_at: datetime
    reset_code: str | None = None


class PasswordResetConfirm(BaseModel):
    email: str
    code: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8)

    @field_validator("code")
    @classmethod
    def _digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Code must contain only digits")
        return v

    @field_validator("new_password")
    @classmethod
    def _password_complexity(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class PasswordResetConfirmResponse(BaseModel):
    detail: str

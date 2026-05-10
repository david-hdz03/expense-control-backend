import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    second_name: str = ""
    paternal_last_name: str = Field(..., min_length=1)
    maternal_last_name: str = ""
    email: str
    password: str = Field(..., min_length=8)
    age: int = Field(..., gt=0)
    currency_code: str = Field(..., min_length=3, max_length=3)

    @field_validator("password")
    @classmethod
    def _password_complexity(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserLogin(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    detail: str
    requires_verification: bool = True
    verification_expires_at: datetime
    verification_code: str | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    is_verified: bool
    is_active: bool
    currency_code: str
    created_at: datetime


class GoogleAuthRequest(BaseModel):
    id_token: str | None = None
    access_token: str | None = None
    platform: Literal["web", "android", "ios"] = "web"

    @field_validator("id_token", mode="before")
    @classmethod
    def _require_at_least_one(cls, v: str | None) -> str | None:
        return v

    def model_post_init(self, __context: object) -> None:
        if not self.id_token and not self.access_token:
            raise ValueError("Either id_token or access_token is required")

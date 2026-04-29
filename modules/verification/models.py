from datetime import datetime, timedelta

from sqlmodel import Field, Relationship, SQLModel

from modules.users.models import User


class VerificationCode(SQLModel, table=True):
    __tablename__ = "verification_codes"
    id: int = Field(default=None, primary_key=True, index=True)
    code: str
    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship()
    attemp_count: int = Field(default=0)
    resended_count: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    expired_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(minutes=15)
    )
    used_at: datetime | None = Field(default=None, nullable=True)


class PasswordResetCode(SQLModel, table=True):
    __tablename__ = "password_reset_codes"
    id: int = Field(default=None, primary_key=True, index=True)
    code: str
    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    used_at: datetime | None = Field(default=None, nullable=True)
    expired_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(minutes=60)
    )

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class UserType(SQLModel, table=True):
    __tablename__ = "usertypes"
    id: int = Field(default=None, primary_key=True, index=True)
    name: str


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    second_name: str = Field(default="")
    paternal_last_name: str
    maternal_last_name: str = Field(default="")
    email: str = Field(unique=True, index=True)
    password: str
    age: int
    currency_code: str
    is_verified: bool = Field(default=False)
    auth_provider: str = Field(default="email")
    is_active: bool = Field(default=True)
    last_login: str = Field(default=None)
    user_type_id: int | None = Field(default=None, foreign_key="usertypes.id")
    user_type: UserType | None = Relationship()
    created_at: str = Field(default=datetime.now)
    updated_at: str = Field(default=datetime.now)

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    age: int
    currency_code: str
    name: str
    second_name: Optional[str] = None
    paternal_last_name: str
    maternal_last_name: str


class UserLogin(UserBase):
    last_login: datetime


class UserDisable(UserBase):
    is_active: bool = False

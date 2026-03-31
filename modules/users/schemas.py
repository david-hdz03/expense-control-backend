from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    age: int
    currency_code: str
    name: str
    second_name: str
    paternal_last_name: str
    maternal_last_name: str
    created_at: str
    updated_at: str


class UserLogin(UserBase):
    last_login: str


class UserDisable(UserBase):
    is_active: bool = False

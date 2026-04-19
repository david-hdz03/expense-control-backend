from datetime import datetime, timedelta

from sqlmodel import Field, Relationship, SQLModel

from modules.users.models import User


class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)
    created_by: int = Field(foreign_key="users.id")
    creator: User = Relationship()

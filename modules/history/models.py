from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from modules.users.models import User


class TransactionChange(SQLModel, table=True):
    __tablename__ = "transaction_changes"
    id: int = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship()
    action: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

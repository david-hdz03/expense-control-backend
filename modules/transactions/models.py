from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from modules.categories.models import Category
from modules.users.models import User


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    id: int = Field(primary_key=True, index=True)
    amount: int
    transaction_type_id: int = Field(foreign_key="transaction_types.id")
    transaction_type: "TransactionType" = Relationship()
    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship()
    category_id: int = Field(default=None, foreign_key="categories.id")
    category: Category = Relationship()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: datetime | None = Field(default=None, nullable=True)


class TransactionTypeCategory(SQLModel, table=True):
    __tablename__ = "transaction_type_categories"
    transaction_type_id: int = Field(
        foreign_key="transaction_types.id", primary_key=True
    )
    category_id: int = Field(foreign_key="categories.id", primary_key=True)


class TransactionType(SQLModel, table=True):
    __tablename__ = "transaction_types"
    id: int = Field(primary_key=True)
    name: str
    disabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    categories: list["Category"] = Relationship(link_model=TransactionTypeCategory)

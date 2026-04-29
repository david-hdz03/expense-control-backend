from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TransactionTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class TransactionBase(BaseModel):
    amount: int
    transaction_type_id: int
    category_id: int | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: int | None = None
    transaction_type_id: int | None = None
    category_id: int | None = None


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: int
    transaction_type: TransactionTypeRead
    category: CategoryRead | None
    user_id: int
    created_at: datetime
    updated_at: datetime

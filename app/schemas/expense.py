from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ExpenseType = Literal["expense", "income"]


class ExpenseBase(BaseModel):
    description: str = Field(..., max_length=255)
    category: str = Field(..., max_length=100)
    amount: Decimal = Field(..., gt=0)
    currency: str = Field("USD", min_length=3, max_length=3)
    type: ExpenseType = "expense"
    spent_at: datetime


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    description: str | None = None
    category: str | None = None
    amount: Decimal | None = None
    currency: str | None = None
    type: ExpenseType | None = None
    spent_at: datetime | None = None


class ExpenseRead(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

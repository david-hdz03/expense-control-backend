from pydantic import BaseModel


class TransactionChangeCreate(BaseModel):
    user_id: int
    action: str

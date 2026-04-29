from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by: int | None = Field(default=None, foreign_key="users.id", nullable=True)

    @property
    def is_default(self) -> bool:
        return self.created_by is None

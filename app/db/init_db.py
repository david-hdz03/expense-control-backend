from app.db.base import Base
from app.db.session import engine
from app.models import Expense, OAuthAccount, User  # noqa: F401 — registra clases en Base.metadata


def init_db() -> None:
    if engine is None:
        return
    Base.metadata.create_all(bind=engine)

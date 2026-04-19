from sqlmodel import SQLModel, Session, create_engine

from core.config import settings

db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
engine = create_engine(db_url)


def get_db():
    with Session(engine) as session:
        yield session

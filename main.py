from fastapi import FastAPI
from sqlalchemy import text

from core.config import settings
from db.base import engine

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
def root():
    return {"project": settings.PROJECT_NAME}


@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}

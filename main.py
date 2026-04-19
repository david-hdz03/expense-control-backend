from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy import text

from core.admin import setup_admin
from core.config import settings
from db.base import engine
from modules.users.router import router as users_router

app = FastAPI(title=settings.PROJECT_NAME)

admin = Admin(app, engine)
setup_admin(admin)


@app.get("/")
def root():
    return {"project": settings.PROJECT_NAME}


@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}


app.include_router(users_router)

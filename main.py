import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from sqlalchemy import text
from sqlmodel import Session, SQLModel

from core.admin import setup_admin
from core.config import settings
from db.all_models import *  # noqa: F401, F403 — registra todos los modelos en SQLModel.metadata
from db.base import engine
from modules.auth.router import router as auth_router
from modules.categories.router import router as categories_router
from modules.categories.service import seed_defaults
from modules.transactions.router import router as transactions_router
from modules.transactions.service import seed_transaction_types
from modules.users.router import router as users_router
from modules.users.service import seed_user_types
from modules.verification.router import router as verification_router


logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        seed_user_types(db)
        seed_defaults(db)
        seed_transaction_types(db)
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=(
        r"^http://(localhost|127\.0\.0\.1)(:\d+)?$" if settings.DEBUG else None
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin = Admin(app, engine)
setup_admin(admin)

app.include_router(auth_router, prefix="/api")
app.include_router(verification_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(transactions_router, prefix="/api")
app.include_router(categories_router, prefix="/api")


@app.get("/")
def root():
    return {"project": settings.PROJECT_NAME}


@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}

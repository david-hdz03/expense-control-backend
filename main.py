from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import text

from core.config import settings
from db.base import engine
from modules.users.models import User
from modules.users.router import router as users_router

#
app = FastAPI(title=settings.PROJECT_NAME)

admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.is_active]
    column_searchable_list = [User.email]
    icon = "fa-solid fa-user"


admin.add_view(UserAdmin)


@app.get("/")
def root():
    return {"project": settings.PROJECT_NAME}


@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}


app.include_router(users_router)

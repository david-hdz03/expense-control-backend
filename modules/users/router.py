# User Router
#
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, insert, select

from core.security import hash_password
from db.base import engine

from .models import User
from .schemas import UserBase, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserBase)
def create_user(user: UserCreate):
    with Session(engine) as session:
        stmt = (
            insert(User)
            .values(
                name=user.name,
                second_name=user.second_name,
                paternal_last_name=user.paternal_last_name,
                maternal_last_name=user.maternal_last_name,
                email=user.email,
                password=hash_password(user.password),
                age=user.age,
                currency_code=user.currency_code,
                user_type_id=user.user_type_id,
            )
            .returning(User)
        )
        result = session.exec(stmt)
        session.commit()
        created_user = result.fetchone()
        if not created_user:
            raise HTTPException(status_code=400, detail="User could not be created")
        return created_user


@router.get("/{user_id}", response_model=UserBase)
def get_user(user_id: int):
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        result = session.exec(stmt)
        user = result.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

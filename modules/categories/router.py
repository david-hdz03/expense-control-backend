from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from core.deps import get_current_user
from db.base import get_db
from modules.users.models import User

from . import service
from .schemas import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
def list_categories(
    transaction_type_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.list_categories(db, current_user.id, transaction_type_id)


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = service.create_category(db, current_user.id, payload)
    if category is None:
        raise HTTPException(status_code=409, detail="Category name already exists")
    return category


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = service.get_category(db, category_id)
    if category is None or category.created_by != current_user.id:
        raise HTTPException(status_code=404, detail="Category not found")
    updated = service.update_category(db, category, current_user.id, payload)
    if updated is None:
        raise HTTPException(status_code=409, detail="Category name already exists")
    return updated


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = service.get_category(db, category_id)
    if category is None or category.created_by != current_user.id:
        raise HTTPException(status_code=404, detail="Category not found")
    service.delete_category(db, category)

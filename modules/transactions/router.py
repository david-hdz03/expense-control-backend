from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from core.deps import get_current_user
from db.base import get_db
from modules.users.models import User

from . import service
from .schemas import TransactionCreate, TransactionRead, TransactionTypeRead, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/types", response_model=list[TransactionTypeRead])
def list_transaction_types(db: Session = Depends(get_db)):
    return service.get_transaction_types(db)


@router.get("", response_model=list[TransactionRead])
def list_transactions(
    transaction_type_id: int | None = None,
    category_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_transactions(db, current_user.id, transaction_type_id, category_id)


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_transaction(db, current_user.id, payload)


@router.get("/{tx_id}", response_model=TransactionRead)
def get_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tx = service.get_transaction(db, tx_id, current_user.id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@router.patch("/{tx_id}", response_model=TransactionRead)
def update_transaction(
    tx_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tx = service.get_transaction(db, tx_id, current_user.id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return service.update_transaction(db, tx, payload)


@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tx = service.get_transaction(db, tx_id, current_user.id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    service.delete_transaction(db, tx)

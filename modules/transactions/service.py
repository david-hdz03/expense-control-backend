from datetime import datetime

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from modules.categories.models import Category

from .models import Transaction, TransactionType, TransactionTypeCategory
from .schemas import TransactionCreate, TransactionUpdate

_TRANSACTION_TYPES = [
    TransactionType(id=1, name="Gastos"),
    TransactionType(id=2, name="Ingresos"),
]

_TYPE_CATEGORIES: dict[int, set[str]] = {
    1: {"Comida", "Salud", "Transporte", "Streaming", "Entretenimiento", "Educación", "Hogar"},
    2: {"Salario", "Freelance", "Inversiones"},
}


def seed_transaction_types(db: Session) -> None:
    exists = db.exec(select(TransactionType).limit(1)).first()
    if exists:
        return

    db.add_all(_TRANSACTION_TYPES)
    db.flush()

    categories = db.exec(select(Category).where(Category.created_by.is_(None))).all()
    name_to_id = {c.name: c.id for c in categories}

    links: list[TransactionTypeCategory] = []
    for type_id, names in _TYPE_CATEGORIES.items():
        for name in names:
            cat_id = name_to_id.get(name)
            if cat_id is not None:
                links.append(TransactionTypeCategory(transaction_type_id=type_id, category_id=cat_id))

    db.add_all(links)
    db.commit()


def get_transaction_types(db: Session) -> list[TransactionType]:
    return list(
        db.exec(select(TransactionType).where(TransactionType.disabled == False))
    )


def _base_query(user_id: int):
    return (
        select(Transaction)
        .options(
            selectinload(Transaction.transaction_type),
            selectinload(Transaction.category),
        )
        .where(Transaction.user_id == user_id, Transaction.deleted_at.is_(None))
    )


def get_transactions(
    db: Session,
    user_id: int,
    transaction_type_id: int | None = None,
    category_id: int | None = None,
) -> list[Transaction]:
    query = _base_query(user_id).order_by(Transaction.created_at.desc())
    if transaction_type_id is not None:
        query = query.where(Transaction.transaction_type_id == transaction_type_id)
    if category_id is not None:
        query = query.where(Transaction.category_id == category_id)
    return list(db.exec(query))


def get_transaction(db: Session, tx_id: int, user_id: int) -> Transaction | None:
    return db.exec(
        _base_query(user_id).where(Transaction.id == tx_id)
    ).first()


def create_transaction(db: Session, user_id: int, payload: TransactionCreate) -> Transaction:
    tx = Transaction(**payload.model_dump(), user_id=user_id)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return db.exec(
        _base_query(tx.user_id).where(Transaction.id == tx.id)
    ).first()


def update_transaction(
    db: Session, tx: Transaction, payload: TransactionUpdate
) -> Transaction:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(tx, key, value)
    tx.updated_at = datetime.now()
    db.add(tx)
    db.commit()
    return db.exec(
        _base_query(tx.user_id).where(Transaction.id == tx.id)
    ).first()


def delete_transaction(db: Session, tx: Transaction) -> None:
    tx.deleted_at = datetime.now()
    tx.updated_at = datetime.now()
    db.add(tx)
    db.commit()

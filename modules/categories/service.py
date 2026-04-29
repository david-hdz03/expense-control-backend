from sqlalchemy import case
from sqlmodel import Session, select

from modules.transactions.models import TransactionTypeCategory
from .models import Category
from .schemas import CategoryCreate, CategoryUpdate

DEFAULT_CATEGORIES = [
    "Comida",
    "Salud",
    "Transporte",
    "Streaming",
    "Entretenimiento",
    "Educación",
    "Hogar",
    "Salario",
    "Freelance",
    "Inversiones",
]


def seed_defaults(db: Session) -> None:
    exists = db.exec(select(Category).where(Category.created_by.is_(None)).limit(1)).first()
    if exists:
        return
    db.add_all([Category(name=name) for name in DEFAULT_CATEGORIES])
    db.commit()


def list_categories(
    db: Session, user_id: int, transaction_type_id: int | None = None
) -> list[Category]:
    query = select(Category).where(
        (Category.created_by.is_(None)) | (Category.created_by == user_id)
    )
    if transaction_type_id is not None:
        query = query.join(
            TransactionTypeCategory,
            TransactionTypeCategory.category_id == Category.id,
        ).where(TransactionTypeCategory.transaction_type_id == transaction_type_id)
    query = query.order_by(
        case((Category.created_by.is_(None), 0), else_=1),
        Category.name,
    )
    return list(db.exec(query))


def get_category(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def create_category(db: Session, user_id: int, payload: CategoryCreate) -> Category | None:
    name = payload.name.strip()
    conflict = db.exec(
        select(Category).where(
            Category.name.ilike(name),
            (Category.created_by.is_(None)) | (Category.created_by == user_id),
        )
    ).first()
    if conflict:
        return None
    category = Category(name=name, created_by=user_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(
    db: Session, category: Category, user_id: int, payload: CategoryUpdate
) -> Category | None:
    name = payload.name.strip()
    conflict = db.exec(
        select(Category).where(
            Category.name.ilike(name),
            (Category.created_by.is_(None)) | (Category.created_by == user_id),
            Category.id != category.id,
        )
    ).first()
    if conflict:
        return None
    category.name = name
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()

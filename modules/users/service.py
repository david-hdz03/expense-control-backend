from sqlmodel import Session, select

from .models import UserType

_DEFAULT_USER_TYPES = [
    UserType(id=1, name="admin"),
    UserType(id=2, name="regular"),
]


def seed_user_types(db: Session) -> None:
    exists = db.exec(select(UserType).limit(1)).first()
    if exists:
        return
    db.add_all(_DEFAULT_USER_TYPES)
    db.commit()

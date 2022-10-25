# type: ignore[call-arg]
from sqlalchemy.orm import Session

from core.hashing import Hasher
from db.models.user import User
from schemas.user import UserCreate


def create_new_user(user: UserCreate, db: Session):
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def retrieve_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    return user

# type: ignore[call-arg]
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.hashing import Hasher
from db.models.user import User
from schemas.users import UserCreate


def repo_create_user(user: UserCreate, db: Session):
    try:
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
    except IntegrityError:
        return None

    return user


def repo_create_superuser(user: UserCreate, db: Session):
    try:
        user = User(
            username=user.username,
            email=user.email,
            hashed_password=Hasher.get_password_hash(user.password),
            is_active=True,
            is_superuser=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        return None

    return user


def repo_get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    return user


def repo_get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    return user


def repo_update_user(user_id: int, changes: UserCreate, db: Session):
    """
    For user to change its own user data. It won't change is_active
    and is_superuser attributes.
    """
    existing_user = db.query(User).filter(User.id == user_id).first()
    existing_user.username = changes.username
    existing_user.hashed_password = Hasher.get_password_hash(changes.password)
    existing_user.email = changes.email
    db.commit()

    return existing_user


def repo_delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()

    return True


def repo_list_users(db: Session):
    users = db.query(User).order_by(User.id).all()
    db.commit()

    return users

# type: ignore[call-arg]
from sqlalchemy.orm import Session

from core.hashing import Hasher
from db.models.user import User
from schemas.user import UserCreate


def repo_create_user(user: UserCreate, db: Session):
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


def repo_create_superuser(user: UserCreate, db: Session):
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

    return user


def repo_get_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    return user


def repo_update_user(user_id: int, user: UserCreate, db: Session):
    """
    For user to change its own user data. It won't change is_active
    and is_superuser attributes.
    """
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        return None  # Maybe is better to raise an error here
    # Hashing password if it's been changed
    if Hasher.verify_password(user.password, existing_user.hashed_password):
        user.password = existing_user.password
    else:
        user.password = Hasher.get_password_hash(user.password)
    # Changing values
    existing_user.username = user.username
    existing_user.hashed_password = user.password
    existing_user.email = user.email
    db.commit()

    return existing_user


def repo_delete_user(user_id: int, db: Session):
    # TODO: this function should raise a proper exception in case it won't
    # find the user to be deleted
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()

    return True

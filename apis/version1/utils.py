from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.orm import Session

from core.config import settings
from core.hashing import Hasher
from db.models.user import User
from db.repository.login import get_user_by_email
from db.session import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    """
    Verify if username (EMAIL!) and password are indeed correct.
    User is accessed by email (email is indexed) and Hasher class
    confirms if password is correct.
    """
    user = get_user_by_email(email=email, db=db)
    if not user:
        return None
    if not Hasher.verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise credentials_exception

    return user

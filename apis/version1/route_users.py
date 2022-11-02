from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .utils import get_current_user_from_token
from db.models.user import User
from db.repository.users import repo_create_superuser
from db.repository.users import repo_create_user
from db.repository.users import repo_delete_user
from db.repository.users import repo_get_user_by_id
from db.repository.users import repo_update_user
from db.session import get_db
from schemas.users import ShowSuperuser
from schemas.users import ShowUser
from schemas.users import UserCreate

router = APIRouter()


@router.post("/create/", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = repo_create_user(user=user, db=db)
    return user


@router.post("/create/super/", response_model=ShowSuperuser)
def create_superuser(
    user: UserCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user_from_token),
):
    user = repo_create_superuser(user=user, db=db)
    return user


@router.get("/get/{user_id}", response_model=ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = repo_get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist",
        )
    return user


@router.put("/update/{user_id}", response_model=ShowUser)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user = repo_update_user(user_id=user_id, user=user, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist",
        )
    return user


@router.delete("/delete/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    if current_user.id == user_id:
        result = repo_delete_user(user_id, db)
        if result:
            return {"detail": f"User with id {user_id} is deleted"}
        else:
            return {"detail": f"User with id {user_id} not found"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not authorized"
    )

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
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
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


@router.put("/update", response_model=ShowUser)
def update_user(
    changes: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    user = repo_update_user(user_id=current_user.id, changes=changes, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {current_user.id} does not exist",
        )
    return user


@router.delete("/delete")
def delete_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    result = repo_delete_user(current_user.id, db)
    if result:
        return {"detail": f"User with id {current_user.id} is deleted"}
    else:
        return {"detail": f"User with id {current_user.id} not found"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not authorized"
    )

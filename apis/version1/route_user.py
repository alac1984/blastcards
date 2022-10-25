from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from db.repository.user import create_new_user
from db.repository.user import retrieve_user
from db.session import get_db
from schemas.user import ShowUser
from schemas.user import UserCreate

router = APIRouter()


@router.post("/create/", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/get/{user_id}", response_model=ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = retrieve_user(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist",
        )
    return user

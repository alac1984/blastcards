from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from .utils import get_current_user_from_token
from db.models.user import User
from db.repository.sets import (
    repo_create_set,
)
from db.session import get_db
from schemas.sets import SetCreate
from schemas.sets import SetShow

router = APIRouter()


@router.post("/create/", response_model=SetShow)
def create_set(
    cardset: SetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    cardset = repo_create_set(cardset, current_user, db)

    return cardset

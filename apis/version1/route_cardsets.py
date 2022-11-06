from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from .utils import get_current_user_from_token
from db.models.user import User
from db.repository.cardsets import (
    repo_create_cardset,
)
from db.session import get_db
from schemas.cardsets import CardsetCreate
from schemas.cardsets import CardsetShow

router = APIRouter()


@router.post("/create", response_model=CardsetShow)
def create_cardset(
    cardset: CardsetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    cardset = repo_create_cardset(cardset, current_user, db)

    return cardset

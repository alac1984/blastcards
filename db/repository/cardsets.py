# type: ignore[call-arg]
from sqlalchemy.orm import Session

from db.models.cardset import Cardset
from db.models.user import User
from schemas.sets import CardsetCreate


def repo_create_cardset(cardset: CardsetCreate, current_user: User, db: Session):
    cardset = Cardset(
        user_id=current_user.id, title=cardset.title, description=cardset.description
    )
    db.add(cardset)
    db.commit()
    db.refresh(cardset)

    return cardset


def repo_list_cardset(current_user: User, db: Session):
    cardsets = db.query(Cardset).filter(Cardset.user_id == current_user.id).all()

    db.commit()
    return cardsets

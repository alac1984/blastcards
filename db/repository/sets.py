# type: ignore[call-arg]
from sqlalchemy.orm import Session

from db.models.set import Set
from db.models.user import User
from schemas.sets import SetCreate


def repo_create_set(cardset: SetCreate, current_user: User, db: Session):
    cardset = Set(
        user_id=current_user.id, title=cardset.title, description=cardset.description
    )
    db.add(cardset)
    db.commit()
    db.refresh(cardset)

    return cardset

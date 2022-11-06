import pytest

from db.repository.cardsets import repo_create_cardset
from schemas.cardsets import CardsetCreate
from db.models.cardset import Cardset
from db.models.user import User


@pytest.mark.integration
def test_repo_create_set(init_db):
    cardset_schema = CardsetCreate(title="Title 1", description="super descriptive")
    user = init_db.query(User).filter(User.id == 1).first()
    cardset = repo_create_cardset(cardset_schema, user, init_db)

    cardset_retrieved = (
        init_db.query(Cardset).filter(Cardset.title == "Title 1").first()
    )

    assert isinstance(cardset, Cardset)
    assert cardset.id == cardset_retrieved.id
    assert cardset.user_id == cardset_retrieved.user_id

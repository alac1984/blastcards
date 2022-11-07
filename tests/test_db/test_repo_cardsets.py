import pytest

from db.models.cardset import Cardset
from db.models.user import User
from db.repository.cardsets import repo_create_cardset
from db.repository.cardsets import repo_list_cardset
from schemas.cardsets import CardsetCreate


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


@pytest.mark.integration
def test_repo_list_cardsets(init_db):
    user = init_db.query(User).filter(User.id == 2).first()
    cardsets = repo_list_cardset(user, init_db)

    assert len(cardsets) == 2
    assert isinstance(cardsets[0], Cardset)

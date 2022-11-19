import pytest
from datetime import datetime

from db.models.cardset import Cardset


@pytest.mark.integration
def test_cardset_repr(init_db):
    cardset = Cardset(
        user_id=1,
        title="test",
        description="test",
        created_on=datetime(1990, 1, 1, 1, 1, 1),
        updated_on=datetime(1990, 1, 1, 1, 1, 1),
    )

    assert (
        cardset.__repr__()
        == "Cardset(id=None, user_id=1, title=test, description=test,"
        " created_on=1990-01-01 01:01:01, updated_on=1990-01-01 01:01:01)"
    )

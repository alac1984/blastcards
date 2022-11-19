from datetime import datetime

import pytest

from db.models.user import User


@pytest.mark.integration
def test_user_repr(init_db):
    user = User(
        username="test",
        email="t@est.com",
        hashed_password="123",
        is_active=False,
        is_superuser=False,
        created_on=datetime(1990, 1, 1, 1, 1, 1),
        updated_on=datetime(1990, 1, 1, 1, 1, 1),
    )

    assert (
        user.__repr__()
        == "User(id=None, username=test, email=t@est.com, is_active=False,"
        " is_superuser=False, created_on=1990-01-01 01:01:01, updated_on=1990-01-01"
        " 01:01:01)"
    )

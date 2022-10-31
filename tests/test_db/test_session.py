import pytest
from db.session import get_db
from sqlalchemy.orm import Session
from typing import Generator


@pytest.mark.integration
def test_get_db():
    db = get_db()
    assert isinstance(db, Generator)
    session = next(db)
    assert isinstance(session, Session)

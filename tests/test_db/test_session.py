from typing import Generator

import pytest
from sqlalchemy.orm import Session

from db.session import get_db


@pytest.mark.integration
def test_get_db():
    db = get_db()
    assert isinstance(db, Generator)
    session = next(db)
    assert isinstance(session, Session)

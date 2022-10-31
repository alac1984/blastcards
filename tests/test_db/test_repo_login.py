import pytest
from db.repository.login import get_user_by_email
from db.models.user import User


@pytest.mark.integration
def test_get_user_by_email(init_db):
    user = get_user_by_email("user@test.com", init_db)

    assert user is not None
    assert isinstance(user, User)
    assert user.email == "user@test.com"

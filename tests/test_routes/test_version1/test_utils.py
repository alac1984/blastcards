import pytest

from apis.version1.utils import authenticate_user
from apis.version1.utils import get_current_user_from_token
from db.models.user import User


@pytest.mark.integration
def test_authenticate_user_success(client, init_db):
    user = authenticate_user("user@test.com", "123456789", init_db)
    assert user is not None
    assert user.username == "user"


@pytest.mark.integration
def test_authenticate_user_fail_pass(client, init_db):
    user = authenticate_user("user@test.com", "12345678910", init_db)  # Wrong password
    assert user is None


@pytest.mark.integration
def test_authenticate_user_fail_email(init_db):
    user = authenticate_user("user@test.com.br", "123456789", init_db)  # Wrong password
    assert user is None


@pytest.mark.integration
def test_get_current_user_from_token(init_db, test_token):
    user = get_current_user_from_token(test_token, db=init_db)
    assert user is not None
    assert isinstance(user, User)

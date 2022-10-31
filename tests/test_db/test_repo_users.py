import pytest
from schemas.users import UserCreate
from core.hashing import Hasher
from db.repository.users import (
    repo_create_user,
    repo_create_superuser,
    repo_get_user_by_id,
    repo_get_user_by_email,
    repo_update_user,
    repo_delete_user,
)
from db.models.user import User


@pytest.mark.integration
def test_repo_create_user(db_session):
    test_user = UserCreate(
        username="testuser", email="testuser@test.com", password="laçksjdfaçlskfj"
    )
    user = repo_create_user(test_user, db_session)
    db_user = db_session.query(User).filter(User.id == 1).first()
    assert isinstance(user, User)
    assert user.id == db_user.id
    assert user.username == db_user.username


@pytest.mark.integration
def test_repo_create_superuser(db_session):
    test_superuser = UserCreate(
        username="testuser",
        email="testuser@test.com",
        password="laçksjdfaçlskfj",
    )
    superuser = repo_create_superuser(test_superuser, db_session)
    db_superuser = db_session.query(User).filter(User.id == 1).first()
    assert isinstance(superuser, User)
    assert superuser.id == db_superuser.id


@pytest.mark.integration
def test_repo_get_user_by_id(init_db):
    test_user = repo_get_user_by_id(user_id=2, db=init_db)
    user = init_db.query(User).filter(User.id == 2).first()
    assert user == test_user


@pytest.mark.integration
def test_repo_get_user_by_email(init_db):
    test_user = repo_get_user_by_email(email="user@test.com", db=init_db)
    user = init_db.query(User).filter(User.email == "user@test.com").first()
    assert user == test_user


@pytest.mark.integration
def test_repo_update_user(init_db):
    changes = UserCreate(
        username="testuser_mod",
        email="testuser_mod@test.com",
        password="modified_pass",
    )

    user_with_changes = repo_update_user(user_id=2, user=changes, db=init_db)

    assert user_with_changes.username == "testuser_mod"
    assert user_with_changes.email == "testuser_mod@test.com"
    assert Hasher.verify_password(changes.password, user_with_changes.hashed_password)


@pytest.mark.integration
def test_repo_delete_user(init_db):
    result = repo_delete_user(user_id=2, db=init_db)
    deleted_user = init_db.query(User).filter(User.id == 2).first()

    assert result
    assert deleted_user is None

from datetime import timedelta

import pytest
from jose import jwt

from core.config import settings
from core.security import create_access_token


@pytest.mark.unit
def test_create_access_token_without_expiredelta():
    data = {"sub": "user@test.com"}
    jwt_token = create_access_token(data)
    decoded = jwt.decode(
        jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert isinstance(jwt_token, str)
    assert decoded["sub"] == "user@test.com"
    assert "exp" in decoded


@pytest.mark.unit
def test_create_access_token_with_expiredelta():
    data = {"sub": "user@test.com"}
    expire_delta = timedelta(seconds=20)
    jwt_token = create_access_token(data, expire_delta)
    decoded = jwt.decode(
        jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert isinstance(jwt_token, str)
    assert decoded["sub"] == "user@test.com"
    assert "exp" in decoded

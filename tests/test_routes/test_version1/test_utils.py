import pytest
from datetime import datetime, timedelta
from jose import jwt
from fastapi import Request
from fastapi.openapi.models import OAuth2
from fastapi.exceptions import HTTPException
from starlette.datastructures import Headers

from apis.version1.utils import authenticate_user
from apis.version1.utils import get_current_user_from_token
from apis.version1.utils import OAuth2PasswordBearerWithCookie
from db.models.user import User
from core.config import settings


@pytest.mark.unit
def test_oauth2passwordbearerwithtoken_instantiation():
    oauth2 = OAuth2PasswordBearerWithCookie("test/testing")
    assert oauth2 is not None
    assert isinstance(oauth2.model, OAuth2)
    assert oauth2.auto_error is True
    assert oauth2.scheme_name == "OAuth2PasswordBearerWithCookie"


@pytest.mark.unit
def test_oauth2passwordbearerwithtoken_call_success(loop, test_token):
    request = Request({"type": "http"})
    request._headers = Headers(
        headers={
            "cookie": (
                f'access_token="Bearer {test_token}"; HttpOnly; Path=/; SameSite=lax'
            )
        }
    )
    oauth2 = OAuth2PasswordBearerWithCookie("test/testing")
    param = loop.run_until_complete(oauth2(request))
    payload = jwt.decode(param, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "user@test.com"


@pytest.mark.unit
def test_oauth2passwordbearerwithtoken_call_fail(loop):
    request = Request({"type": "http"})
    request._headers = Headers()
    oauth2 = OAuth2PasswordBearerWithCookie("test/testing")
    # As we do not have an authorization cookie, it will throw an HTTPException
    with pytest.raises(HTTPException):
        loop.run_until_complete(oauth2(request))


@pytest.mark.unit
def test_oauth2passwordbearerwithtoken_call_autoerror(loop):
    request = Request({"type": "http"})
    request._headers = Headers()
    oauth2 = OAuth2PasswordBearerWithCookie("test/testing", auto_error=False)
    # As we do not have an authorization cookie and auto_error is False,
    # it will return None
    param = loop.run_until_complete(oauth2(request))
    assert param is None


@pytest.mark.integration
def test_authenticate_user_success(client, init_db):
    user = authenticate_user("user@test.com", "123456789", init_db)
    assert user is not None
    assert user.username == "user"


@pytest.mark.integration
def test_authenticate_user_fail_pass(client, init_db):
    user = authenticate_user(
        "user@test.com", "12345678910", init_db
    )  # Wrong password
    assert user is None


@pytest.mark.integration
def test_authenticate_user_fail_email(init_db):
    user = authenticate_user(
        "user039049403@test.com.br", "123456789", init_db
    )  # Wrong email
    assert user is None


@pytest.mark.integration
def test_get_current_user_from_token_success(init_db, test_token):
    user = get_current_user_from_token(test_token, db=init_db)
    assert user is not None
    assert isinstance(user, User)


@pytest.mark.integration
def test_get_current_user_from_token_no_user(init_db):
    expire = datetime.utcnow() + timedelta(seconds=20)
    to_encode = {"sub": "", "exp": expire}
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    with pytest.raises(HTTPException) as exc:
        get_current_user_from_token(token, db=init_db)

    assert exc.value.status_code == 401


@pytest.mark.integration
def test_get_current_user_from_token_no_email(init_db):
    expire = datetime.utcnow() + timedelta(seconds=20)
    to_encode = {"exp": expire}
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    with pytest.raises(HTTPException) as exc:
        get_current_user_from_token(token, db=init_db)

    assert exc.value.status_code == 401


@pytest.mark.integration
def test_get_current_user_from_token_jwt_error(init_db):
    expire = datetime.utcnow() + timedelta(seconds=20)
    to_encode = {"exp": expire}
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    error_token = token[:-1]
    with pytest.raises(HTTPException) as exc:
        get_current_user_from_token(error_token, db=init_db)

    assert exc.value.status_code == 401

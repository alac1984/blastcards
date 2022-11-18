import pytest
from fastapi import Response
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from apis.version1.route_login import login_for_access_token


@pytest.mark.integration
def test_login_for_access_token_success(client, init_db):
    class FormData(BaseModel):
        username: str
        password: str

    response = Response()
    form_data = FormData(username="user@test.com", password="123456789")
    access_token = login_for_access_token(response, form_data, init_db)

    assert isinstance(access_token, dict)
    assert isinstance(access_token["access_token"], str)
    assert access_token["token_type"] == "bearer"


@pytest.mark.integration
def test_login_for_access_token_no_user(client, init_db):
    class FormData(BaseModel):
        username: str
        password: str

    response = Response()
    # A username and password not inserted on database
    form_data = FormData(username="user@test039302.com", password="123456789")

    with pytest.raises(HTTPException) as exc:
        login_for_access_token(response, form_data, init_db)
        assert exc.status_code == 401
        assert exc.detail == "Incorrect username or password"

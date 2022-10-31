import pytest
from pydantic import BaseModel
from apis.version1.route_login import login_for_access_token


@pytest.mark.integration
def test_login_for_access_token(client, init_db):
    class FormData(BaseModel):
        username: str
        password: str

    form_data = FormData(username="user@test.com", password="123456789")
    access_token = login_for_access_token(form_data, init_db)

    assert isinstance(access_token, dict)
    assert isinstance(access_token["access_token"], str)
    assert access_token["token_type"] == "bearer"

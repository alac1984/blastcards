import json

import pytest


@pytest.mark.integration
def test_create_cardset(client, init_db, auth_cookie):
    data = {"title": "A cardset", "description": "A cardset's description"}

    response = client.post("cardsets/create", json.dumps(data), cookies=auth_cookie)

    assert response.status_code == 200
    assert response.json()["user_id"] == 2
    assert response.json()["title"] == "A cardset"


@pytest.mark.integration
def test_cardset_get_all(client, init_db, auth_cookie):
    response = client.get("cardsets/get/all", cookies=auth_cookie)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert isinstance(response.json()[0], dict)

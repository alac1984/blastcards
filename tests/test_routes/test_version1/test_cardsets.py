import json
import pytest


@pytest.mark.integration
def test_create_cardset(client, init_db, auth_headers):
    data = {"title": "A cardset", "description": "A cardset's description"}

    response = client.post("cardsets/create", json.dumps(data), headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["user_id"] == 2
    assert response.json()["title"] == "A cardset"

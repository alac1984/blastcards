import json


def test_create_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "testing",
    }
    response = client.post("/user/create/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@email.com"
    assert response.json()["is_active"] is True


def test_retrieve_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "testing",
    }
    response = client.post("/user/create/", json.dumps(data))
    response = client.get("user/get/1")

    assert response.status_code == 200
    assert response.json()["email"] == "testuser@email.com"

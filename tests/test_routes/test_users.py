import json

import pytest


@pytest.mark.integration
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


@pytest.mark.integration
def test_create_superuser(client):
    data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "testing",
    }
    response = client.post("/user/create/super/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@email.com"
    assert response.json()["is_active"] is True
    assert response.json()["is_superuser"] is True


@pytest.mark.integration
def test_get_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "testing",
    }
    response = client.post("/user/create/", json.dumps(data))
    response = client.get("user/get/1")

    assert response.status_code == 200
    assert response.json()["email"] == "testuser@email.com"


@pytest.mark.integration
def test_update_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "testing",
    }
    response = client.post("/user/create/", json.dumps(data))
    data_changed = {
        "username": "testuser_changed",
        "email": "testuser_changed@email.com",
        "password": "testing_changed",
    }
    response = client.put("user/update/1", json.dumps(data_changed))
    assert response.status_code == 200
    assert response.json()["username"] == "testuser_changed"
    assert response.json()["email"] == "testuser_changed@email.com"

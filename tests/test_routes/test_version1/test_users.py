import json

import pytest


@pytest.mark.integration
def test_create_user_success(client, init_db):
    data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "testing",
    }
    response = client.post("/users/create/", json.dumps(data))
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@email.com"
    assert response.json()["is_active"] is True


@pytest.mark.integration
def test_create_user_fail(client, init_db):
    data = {
        "username": "user",
        "email": "user@test.com",
        "password": "testing",
    }
    response = client.post("/users/create/", json.dumps(data))
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this username already exists"


@pytest.mark.integration
def test_create_superuser_success(client, init_db):
    data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "testing",
    }
    response = client.post("/users/create/super/", json.dumps(data))
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@email.com"
    assert response.json()["is_active"] is True
    assert response.json()["is_superuser"] is True


@pytest.mark.integration
def test_create_superuser_fail(client, init_db):
    data = {
        "username": "superuser",
        "email": "superuser@test.com",
        "password": "testing",
    }

    response = client.post("/users/create/super/", json.dumps(data))
    assert response.status_code == 400
    assert response.json()["detail"] == "Superuser with this username already exists"


@pytest.mark.integration
def test_get_user_success(client, init_db):
    response = client.get("users/get/1")

    assert response.status_code == 200
    assert response.json()["email"] == "superuser@test.com"


@pytest.mark.integration
def test_get_user_fail(client, init_db):
    response = client.get("users/get/999")

    assert response.status_code == 404


@pytest.mark.integration
def test_update_user_success(client, init_db, auth_cookie):
    data_changed = {
        "username": "testuser_changed",
        "email": "testuser_changed@test.com",
        "password": "testing_changed",
    }
    response = client.put(
        "users/update", json.dumps(data_changed), cookies=auth_cookie
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser_changed"
    assert response.json()["email"] == "testuser_changed@test.com"


@pytest.mark.integration
def test_delete_user(client, init_db, auth_cookie):
    response = client.delete("/users/delete", cookies=auth_cookie)
    assert response.status_code == 204
    assert response.content == b"User with id 2 is deleted"


@pytest.mark.integration
def test_list_users(client, init_db):
    response = client.get("/users/get/all")
    assert response.status_code == 200
    assert len(response.json()) == 2

import pytest


@pytest.mark.integration
def test_webapp_login_get(client, init_db):
    response = client.get("/login")

    assert response.status_code == 200


def test_webapp_login_post_success(client, init_db):
    response = client.post(
        "/login", data={"email": "user@test.com", "password": "123456789"}
    )

    assert response.status_code == 200
    assert b"Dashboard" in response.content


def test_webapp_login_post_fail_email(client, init_db):
    response = client.post(
        "/login", data={"email": "usertest.com", "password": "a1k8u2"}
    )

    assert response.status_code == 200
    assert b"Invalid email format" in response.content


def test_webapp_login_post_fail_pass(client, init_db):
    response = client.post(
        "/login", data={"email": "user@test.com", "password": "a1k8u"}
    )

    assert response.status_code == 200
    assert b"Incorrect email or password" in response.content

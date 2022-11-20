import pytest


@pytest.mark.unit
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

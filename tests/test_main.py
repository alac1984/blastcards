import pytest
from fastapi import FastAPI

import main


@pytest.fixture
def test_app():
    app = FastAPI()
    return app


@pytest.mark.unit
def test_include_router(test_app):
    main.include_router(test_app)
    routes = [route.name for route in test_app.routes]
    assert "home" in routes
    assert "create_user" in routes
    assert "login_for_access_token" in routes
    assert "login" in routes


@pytest.mark.unit
def test_configure_static(test_app):
    main.configure_static(test_app)
    routes = [route.name for route in test_app.routes]
    assert "static" in routes


@pytest.mark.unit
def test_start_application():
    app = main.start_application()
    routes = [route.name for route in app.routes]
    assert "home" in routes
    assert "create_user" in routes
    assert "login_for_access_token" in routes
    assert "login" in routes
    assert "static" in routes

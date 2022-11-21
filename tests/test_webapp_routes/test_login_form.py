import pytest
from fastapi import Request
from starlette.datastructures import FormData
from starlette.datastructures import Headers

from webapps.login.forms import LoginForm


@pytest.mark.unit
def test_login_form_instantiation():
    request = Request({"type": "http"})
    form = LoginForm(request)

    assert form is not None
    assert form.errors == []
    assert form.username is None
    assert form.password is None


@pytest.mark.unit
def test_login_form_load_data(loop):
    request = Request({"type": "http"})
    request._form = FormData({"email": "user@test.com", "password": "a1k8u2"})
    request._headers = Headers({"Content-Type": "application/x-www-form-urlencoded"})
    form = LoginForm(request)
    loop.run_until_complete(form.load_data())

    assert form.username == "user@test.com"
    assert form.password == "a1k8u2"


@pytest.mark.unit
def test_login_form_is_valid_true(loop):
    request = Request({"type": "http"})
    request._form = FormData({"email": "user@test.com", "password": "a1k8u2"})
    request._headers = Headers({"Content-Type": "application/x-www-form-urlencoded"})
    form = LoginForm(request)
    loop.run_until_complete(form.load_data())

    assert loop.run_until_complete(form.is_valid())


@pytest.mark.unit
def test_login_form_is_valid_false_email_wrong(loop):
    request = Request({"type": "http"})
    request._form = FormData({"email": "usertest.com", "password": "a1k8u2"})
    request._headers = Headers({"Content-Type": "application/x-www-form-urlencoded"})
    form = LoginForm(request)
    loop.run_until_complete(form.load_data())

    assert loop.run_until_complete(form.is_valid()) is False
    assert "Invalid email format" in form.errors


@pytest.mark.unit
def test_login_form_is_valid_false_no_password(loop):
    request = Request({"type": "http"})
    request._form = FormData({"email": "user@test.com", "password": "a"})
    request._headers = Headers({"Content-Type": "application/x-www-form-urlencoded"})
    form = LoginForm(request)
    loop.run_until_complete(form.load_data())

    assert loop.run_until_complete(form.is_valid()) is False
    assert "Invalid password format" in form.errors

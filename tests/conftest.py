import asyncio
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apis.base import api_router
from core.config import settings
from core.hashing import Hasher
from db.base import Base
from db.models.cardset import Cardset
from db.models.user import User
from db.session import get_db
from webapps.base import webapp_router


def start_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    app.include_router(webapp_router)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case
    """
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    # transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use this session in tests
    session.close()
    # This rollback below was giving me warnings at pytest
    # transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the "db_session" fixture
    to override the 'get_db' dependency that is injected into routes
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def init_db(db_session):
    """
    To be used by all tests that need some initial data
    """
    hashed_password = Hasher.get_password_hash("123456789")
    superuser = User(
        username="superuser",
        email="superuser@test.com",
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False,
    )
    user = User(
        username="user",
        email="user@test.com",
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=True,
    )
    cset1 = Cardset(
        user_id=1,
        title="Set 1",
        description="Descriptive set",
    )
    cset2 = Cardset(user_id=2, title="Set 2")
    cset3 = Cardset(user_id=2, title="Set 3")
    objects = [superuser, user, cset1, cset2, cset3]
    db_session.bulk_save_objects(objects)
    db_session.flush()
    yield db_session


@pytest.fixture(scope="module")
def test_token():
    expire = datetime.utcnow() + timedelta(seconds=20)
    to_encode = {"sub": "user@test.com", "exp": expire}
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token


# @pytest.fixture(scope="module")
# def auth_headers(test_token):  # Auth headers for user2
#     headers = {"Authorization": f"Bearer {test_token}"}
#     return headers


@pytest.fixture(scope="module")
def auth_cookie(test_token):
    return {"access_token": f"Bearer {test_token}"}


@pytest.fixture(scope="function")
def loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

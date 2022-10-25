from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine


def include_router(app: FastAPI) -> None:
    app.include_router(api_router)


def configure_static(app: FastAPI) -> None:
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(engine)


def start_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    configure_static(app)
    include_router(app)
    create_tables()
    return app


app = start_application()

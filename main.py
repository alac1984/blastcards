from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apis.base import api_router
from webapps.base import webapp_router
from core.config import settings


def include_router(app: FastAPI) -> None:
    app.include_router(api_router)
    app.include_router(webapp_router)


def configure_static(app: FastAPI) -> None:
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    configure_static(app)
    include_router(app)
    return app


app = start_application()

from fastapi import APIRouter

from webapps.login import route_login
from webapps.home import route_home


webapp_router = APIRouter()
webapp_router.include_router(route_home.router, prefix="", tags=["home-webapp"])
webapp_router.include_router(route_login.router, prefix="", tags=["login-webapp"])

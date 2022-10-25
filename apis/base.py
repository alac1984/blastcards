from fastapi import APIRouter

from apis.version1 import route_general_pages
from apis.version1 import route_user


api_router = APIRouter()

api_router.include_router(route_general_pages.router, prefix="", tags=["general_pages"])

api_router.include_router(route_user.router, prefix="/user", tags=["users"])

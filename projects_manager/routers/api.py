from fastapi import APIRouter
from projects_manager.routers.projects import projects_router

router = APIRouter()

API_PREFIX = "/api"


def include_api_routes():
    router.include_router(projects_router, prefix=API_PREFIX)


include_api_routes()

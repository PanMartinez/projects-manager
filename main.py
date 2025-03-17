from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from projects_manager.config.db import engine, SessionLocal
from projects_manager.config.settings import get_settings
from projects_manager.domain.common.models import Base
from projects_manager.handlers import http_error_handler
from projects_manager.routers.api import router as api_router


def get_application() -> FastAPI:
    application = FastAPI()
    Base.metadata.create_all(bind=engine)
    application.include_router(api_router)
    application.add_exception_handler(Exception, http_error_handler)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    add_pagination(application)
    return application


app = get_application()


@app.middleware("http")
def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    try:
        response = call_next(request)
    finally:
        request.state.db.close()
    return response

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


def http_error_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return JSONResponse(
            {"errors": [exc.detail]},
            status_code=exc.status_code,
        )
    return JSONResponse(
        {"errors": ["An unexpected error occurred."]},
        status_code=500,
    )


class ErrorMessages:
    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"

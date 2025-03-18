from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


def http_error_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return JSONResponse(
            {"errors": [exc.detail]},
            status_code=exc.status_code,
        )

    if isinstance(exc, IntegrityError):
        error_message = str(exc.orig)

        if "check_start_end_date" in error_message:
            return JSONResponse(
                {"errors": ["start_date must be before or equal to end_date."]},
                status_code=400,
            )

        return JSONResponse(
            {"errors": ["A database integrity error occurred."]},
            status_code=400,
        )

    return JSONResponse(
        {"errors": ["An unexpected error occurred."]},
        status_code=500,
    )


class ErrorMessages:
    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"

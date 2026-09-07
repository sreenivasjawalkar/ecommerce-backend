from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ApplicationError,
    AuthenticationError,
    AuthorizationError,
    InactiveUserError,
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)


def application_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    if not isinstance(exc, ApplicationError):
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred.",
                }
            },
        )

    status_code = 500

    if isinstance(exc, ResourceNotFoundError):
        status_code = 404

    elif isinstance(exc, ResourceAlreadyExistsError):
        status_code = 409

    elif isinstance(exc, InactiveUserError):
        status_code = 403

    elif isinstance(exc, AuthenticationError):
        status_code = 401

    elif isinstance(exc, AuthorizationError):
        status_code = 403

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )
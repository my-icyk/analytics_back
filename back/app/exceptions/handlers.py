"""
Exception -> HTTP response mapping.

`@app.exception_handler(...)` must be called on a real FastAPI instance.
Since this module doesn't create the app, it can't decorate at import time —
instead it exposes `register_exception_handlers(app)`, which main.py calls
once it has created `app`.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    AlreadyExistsError,
    ForbiddenError,
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
    NotFoundError,
    PasswordMismatchError,
    UserNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserNotFoundError)
    def user_not_found_handler(_request: Request, exc: UserNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AlreadyExistsError)
    def already_exists_handler(_request: Request, exc: AlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ForbiddenError)
    def forbidden_handler(_request: Request, exc: ForbiddenError):
        return JSONResponse(
            status_code=403,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    def generic_exception_handler(_request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotFoundError)
    def not_found_error_handler(_request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AlreadyExistsError)
    def already_exists_error_handler(_request: Request, exc: AlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidCredentialsError)
    def invalid_credentials_handler(_request: Request, exc: InvalidCredentialsError):
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(InvalidTokenError)
    def invalid_token_handler(_request: Request, exc: InvalidTokenError):
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(InactiveUserError)
    def inactive_user_handler(_request: Request, exc: InactiveUserError):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(PasswordMismatchError)
    def password_mismatch_handler(_request: Request, exc: PasswordMismatchError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

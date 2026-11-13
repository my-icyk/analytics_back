from fastapi import APIRouter, Depends, Response

from app.api.deps import (
    get_auth_service,
    session_cookie,
)
from app.config import get_settings
from app.schemas.auth_schemas import LoginRequest
from app.services.auth.authentication_service import AuthenticationService

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


print(settings.SESSION_LIFETIME)

print(settings.SESSION_COOKIE_NAME, settings.COOKIE_SECURE)


@router.post("/login", status_code=204)
def login(
    payload: LoginRequest,
    response: Response,
    service: AuthenticationService = Depends(get_auth_service),
) -> None:
    token = service.login(payload.username, payload.password)
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=token,
        max_age=int(settings.SESSION_LIFETIME.total_seconds()),
        path="/",
        secure=settings.COOKIE_SECURE,
        httponly=True,
        samesite="lax",
    )


@router.post("/logout", status_code=204)
def logout(
    response: Response,
    token: str | None = Depends(session_cookie),
    service: AuthenticationService = Depends(get_auth_service),
) -> None:
    service.logout(token)
    response.delete_cookie(
        key=settings.SESSION_COOKIE_NAME,
        path="/",
        secure=settings.COOKIE_SECURE,
        httponly=True,
        samesite="lax",
    )

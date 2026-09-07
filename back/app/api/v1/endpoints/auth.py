from datetime import datetime

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_service
from app.config import get_settings
from app.exceptions.exceptions import InvalidTokenError
from app.schemas.auth_schemas import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

REFRESH_COOKIE_NAME = "refresh_token"
# Cookie is scoped to /auth so it's never sent on unrelated API calls —
# only the login/refresh/logout endpoints ever see it.
REFRESH_COOKIE_PATH = "/auth"


def _set_refresh_cookie(response: Response, token: str, expires_at: datetime) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=token,
        httponly=True,  # not readable by JS -> mitigates XSS token theft
        secure=settings.COOKIE_SECURE,  # see config.py: must be True in production
        samesite="lax",
        expires=expires_at,
    )


@router.post("/token", response_model=TokenResponse, include_in_schema=False)
def login_for_swagger(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    """
    Form-encoded login, used only by Swagger UI's 'Authorize' button
    (which sends application/x-www-form-urlencoded, not JSON). Same
    AuthService.login() underneath — no logic duplicated. Hidden from the
    schema (include_in_schema=False) so it doesn't show up as a second,
    confusing '/login' option in the docs.
    """
    access_token, refresh_token, expires_at = service.login(
        form_data.username, form_data.password
    )
    _set_refresh_cookie(response, refresh_token, expires_at)
    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    access_token, refresh_token, expires_at = service.login(
        payload.username, payload.password
    )
    _set_refresh_cookie(response, refresh_token, expires_at)
    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    raw_refresh = request.cookies.get(REFRESH_COOKIE_NAME)
    if raw_refresh is None:
        raise InvalidTokenError()

    access_token, new_refresh, expires_at = service.refresh(raw_refresh)
    _set_refresh_cookie(response, new_refresh, expires_at)
    return TokenResponse(access_token=access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    raw_refresh = request.cookies.get(REFRESH_COOKIE_NAME)
    if raw_refresh:
        service.logout(raw_refresh)
    response.delete_cookie(REFRESH_COOKIE_NAME, path=REFRESH_COOKIE_PATH)

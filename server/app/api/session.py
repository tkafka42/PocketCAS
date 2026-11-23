"""Anmelden und Abmelden mit dem gemeinsamen Passwort."""

import asyncio
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response

from ..auth import COOKIE_NAME, create_token, password_matches, token_is_valid
from ..config import Settings, get_settings
from ..errors import AppError
from ..schemas import LoginRequest, SessionStatus

router = APIRouter(prefix="/api", tags=["session"])
_FAILED_LOGIN_DELAY_SECONDS = 0.5


@router.post("/login", response_model=SessionStatus)
async def login(
    payload: LoginRequest,
    response: Response,
    settings: Annotated[Settings, Depends(get_settings)],
) -> SessionStatus:
    if not password_matches(payload.password, settings):
        await asyncio.sleep(_FAILED_LOGIN_DELAY_SECONDS)
        raise AppError(401, "WRONG_PASSWORD", "Das Passwort stimmt nicht.")
    response.set_cookie(
        COOKIE_NAME,
        create_token(settings),
        max_age=settings.session_hours * 3600,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
        path="/",
    )
    return SessionStatus(authenticated=True)


@router.post("/logout", response_model=SessionStatus)
def logout(response: Response) -> SessionStatus:
    response.delete_cookie(COOKIE_NAME, path="/")
    return SessionStatus(authenticated=False)


@router.get("/session", response_model=SessionStatus)
def session_status(
    settings: Annotated[Settings, Depends(get_settings)],
    session_token: Annotated[str | None, Cookie(alias=COOKIE_NAME)] = None,
) -> SessionStatus:
    return SessionStatus(authenticated=token_is_valid(session_token, settings))

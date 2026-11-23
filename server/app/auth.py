"""Einfacher Schutz mit einem gemeinsamen Passwort und signiertem Session-Cookie."""

import hashlib
import hmac
import time
from typing import Annotated

from fastapi import Cookie, Depends

from .config import Settings, get_settings
from .errors import AppError

COOKIE_NAME = "pocketcas_session"


def _signature(payload: str, settings: Settings) -> str:
    # Das Passwort fließt in den Schlüssel ein: Eine Änderung beendet alle Sitzungen.
    key = (settings.auth_secret.get_secret_value() + settings.app_password.get_secret_value()).encode()
    return hmac.new(key, payload.encode(), hashlib.sha256).hexdigest()


def password_matches(candidate: str, settings: Settings) -> bool:
    return hmac.compare_digest(candidate.encode(), settings.app_password.get_secret_value().encode())


def create_token(settings: Settings) -> str:
    payload = str(int(time.time()) + settings.session_hours * 3600)
    return f"{payload}.{_signature(payload, settings)}"


def token_is_valid(token: str | None, settings: Settings) -> bool:
    if not token:
        return False
    payload, _, signature = token.partition(".")
    if not payload.isascii() or not payload.isdigit():
        return False
    if not hmac.compare_digest(signature.encode(), _signature(payload, settings).encode()):
        return False
    return int(payload) > time.time()


def require_auth(
    settings: Annotated[Settings, Depends(get_settings)],
    session_token: Annotated[str | None, Cookie(alias=COOKIE_NAME)] = None,
) -> None:
    if not token_is_valid(session_token, settings):
        raise AppError(401, "UNAUTHORIZED", "Bitte melde dich mit dem Passwort an.")

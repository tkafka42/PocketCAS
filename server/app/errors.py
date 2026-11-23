"""Einheitliche API-Fehler: immer { code, message }, Texte auf Deutsch."""

from typing import Any


class AppError(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        *,
        position: int | None = None,
        current: Any = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.position = position
        self.current = current

    def body(self) -> dict[str, Any]:
        data: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.position is not None:
            data["position"] = self.position
        if self.current is not None:
            data["current"] = self.current
        return data

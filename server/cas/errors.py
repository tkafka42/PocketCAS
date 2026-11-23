"""Übersetzt Engine-Fehler in Fehlercodes und deutsche Meldungen."""

import re

from .engine.core.errors import (
    ArgumentError,
    CalcError,
    CalcSyntaxError,
    DomainError,
    UndefinedError,
)

_SYNTAX_MESSAGES: tuple[tuple[str, str], ...] = (
    (r"Missing \)", "Klammer nicht geschlossen. Es fehlt eine „)“."),
    (r"Missing \]", "Eckige Klammer nicht geschlossen. Es fehlt eine „]“."),
    (r"Missing \}", "Geschweifte Klammer nicht geschlossen. Es fehlt eine „}“."),
    (r'Missing closing "', "Text nicht geschlossen. Es fehlt ein Anführungszeichen."),
    (r"Empty input", "Die Eingabe ist leer."),
    (r"Unexpected end of input", "Die Eingabe endet zu früh. Prüfe den Schluss des Ausdrucks."),
    (r"Missing operator between numbers", "Zwischen zwei Zahlen fehlt ein Rechenzeichen."),
    (r"Unexpected character", "Die Eingabe enthält ein ungültiges Zeichen."),
    (r"Unexpected '", "An dieser Stelle passt das Zeichen nicht."),
    (r"Variable name expected", "Hier wird ein Variablenname erwartet."),
    (r"Index expected", "Hier wird ein Index erwartet."),
    (r"Dimension error", "Alle Zeilen der Matrix müssen gleich lang sein."),
    (r"Conversion target expected", "Nach ► fehlt das Ziel der Umrechnung."),
)

_OTHER_MESSAGES: tuple[tuple[str, str], ...] = (
    (r"Too few arguments", "Zu wenige Argumente für diesen Befehl."),
    (r"Too many arguments", "Zu viele Argumente für diesen Befehl."),
    (r"Dimension mismatch", "Die Größen der Listen oder Matrizen passen nicht zusammen."),
    (r"[Nn]on-real", "Das Ergebnis ist nicht reell. Stelle bei Bedarf den Komplex-Modus ein."),
    (r"string is not allowed|Data type", "Dieser Datentyp ist hier nicht erlaubt."),
    (r"is not defined", "Eine Variable hat noch keinen Wert."),
    (r"Incompatible units", "Diese Einheiten lassen sich nicht ineinander umrechnen."),
    (r"[Dd]ivision by zero|[Dd]ivide by zero", "Division durch null ist nicht definiert."),
    (r"not connected", "Dieser Befehl braucht Zusatz-Hardware und ist hier nicht verfügbar."),
)


def _translate(message: str, table: tuple[tuple[str, str], ...]) -> str | None:
    for pattern, german in table:
        if re.search(pattern, message):
            return german
    return None


def describe_error(error: CalcError) -> dict:
    """Liefert Code, Meldung und Position, nie einen Stacktrace."""
    if isinstance(error, CalcSyntaxError):
        message = _translate(error.message, _SYNTAX_MESSAGES) or "Die Eingabe enthält einen Syntaxfehler."
        return {"code": "SYNTAX_ERROR", "message": message, "position": error.position}

    german = _translate(error.message, _OTHER_MESSAGES)
    if "not connected" in error.message:
        return {"code": "UNSUPPORTED", "message": german, "position": None}
    if isinstance(error, ArgumentError):
        fallback = "Die Argumente passen nicht zu diesem Befehl."
    elif isinstance(error, DomainError):
        fallback = "Der Wert liegt außerhalb des erlaubten Bereichs."
    elif isinstance(error, UndefinedError):
        fallback = "Ein Name ist nicht definiert."
    else:
        fallback = "Das lässt sich nicht berechnen."
    return {"code": "MATH_ERROR", "message": german or fallback, "position": error.position}

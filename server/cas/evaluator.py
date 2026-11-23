"""Führt eine Berechnung mit der Engine aus. Läuft nur im Worker-Prozess."""

from typing import Any

import sympy as sp

from .engine.core.errors import CalcError
from .engine.core.formatting import stat_table
from .engine.core.latex import value_latex
from .engine.core.session import Session, Settings
from .engine.core.values import ListValue, SolveResult, StatResults
from .engine.functions import lookup_builtin
from .errors import describe_error

_SOLVE_COMMANDS = {"solve", "csolve", "nsolve", "zeros", "czeros"}


def build_source(expression: str, command: str | None, arguments: list[str]) -> str:
    """Setzt den Aufruf genau in der Syntax von complex_calc zusammen."""
    if not command:
        return expression
    spec = lookup_builtin(command)
    if spec is None:
        raise KeyError(command)
    joined = ",".join([expression, *arguments])
    return f"{spec.name} {joined}" if spec.command else f"{spec.name}({joined})"


def _is_no_solution(value: Any, command: str | None) -> bool:
    if not command or command.lower() not in _SOLVE_COMMANDS:
        return False
    if isinstance(value, SolveResult):
        return not (value.alternatives or value.intervals or value.always_true or value.general)
    return value is sp.false or (isinstance(value, ListValue) and not value)


def _latex(value: Any, settings: Settings) -> str | None:
    return value_latex(value, settings)


def _new_session(job: dict) -> Session:
    options = job["options"]
    settings = Settings(
        angle=options["angle"],
        mode=options["mode"],
        complex_format=options["complex_format"],
        letters_are_constants=options["letters_are_constants"],
    )
    # Eingabe-Befehle wie Request werden am Server abgebrochen.
    session = Session(settings=settings, input_provider=lambda prompt, is_string: None)
    for statement in job["context"]:
        session.run(statement)
    return session


def _decimal(job: dict, source: str, exact_text: str) -> str | None:
    try:
        session = _new_session(job)
        text = session.format(session.evaluate(source, force_approx=True))
    except Exception:  # noqa: BLE001 - nicht jedes Ergebnis hat eine Dezimalform
        return None
    return None if text == exact_text else text


def evaluate_job(job: dict) -> dict:
    try:
        source = build_source(job["expression"], job["command"], job["arguments"])
    except KeyError:
        return {"ok": False, "code": "UNSUPPORTED", "message": "Diesen Befehl gibt es nicht.", "position": None}

    session = _new_session(job)
    session._output = []
    session.canvas = None
    try:
        value = session.evaluate(source)
    except CalcError as error:
        return {"ok": False, **describe_error(error)}
    except RecursionError:
        return {"ok": False, "code": "TOO_LARGE", "message": "Der Ausdruck ist zu tief verschachtelt.", "position": None}
    except ZeroDivisionError:
        return {"ok": False, "code": "MATH_ERROR", "message": "Division durch null ist nicht definiert.", "position": None}
    except (TypeError, ValueError, NotImplementedError, AttributeError, IndexError, KeyError, OverflowError):
        return {"ok": False, "code": "MATH_ERROR", "message": "Das lässt sich nicht berechnen.", "position": None}

    text = session.format(value)
    output = list(session._output)
    drawing = list(session.canvas.ops) if session.canvas is not None else []
    table = stat_table(value, session.settings) if isinstance(value, StatResults) else None
    # Programme nicht doppelt ausführen, wenn sie Ausgaben oder Zeichnungen erzeugen.
    decimal = None if output or drawing or table else _decimal(job, source, text)
    return {
        "ok": True,
        "source": source,
        "status": "no_solution" if _is_no_solution(value, job["command"]) else "solved",
        "text": text,
        "latex": _latex(value, session.settings),
        "decimal": decimal,
        "table": table,
        "output": output,
        "drawing": drawing,
    }

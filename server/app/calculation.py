"""Verbindet die API mit dem isolierten CAS-Worker."""

from cas.worker import WorkerLimits, run_job

from .config import Settings
from .errors import AppError
from .schemas import CalcOptions, EvaluationRequest, EvaluationResponse

_STATUS_BY_CODE = {"TIMEOUT": 504, "BUSY": 503}


def limits_from(settings: Settings) -> WorkerLimits:
    return WorkerLimits(settings.cas_timeout_seconds, settings.cas_memory_mb, settings.cas_max_workers)


def calculate(request: EvaluationRequest, settings: Settings) -> EvaluationResponse:
    result = run_job(
        {
            "expression": request.expression,
            "command": request.command,
            "arguments": request.arguments,
            "context": request.context,
            "options": request.options.model_dump(),
        },
        limits_from(settings),
    )
    if not result.pop("ok"):
        raise AppError(
            _STATUS_BY_CODE.get(result["code"], 422),
            result["code"],
            result["message"],
            position=result.get("position"),
        )
    return EvaluationResponse(**result)


def recalculate(expression: str, command: str | None, arguments: list[str], settings: Settings) -> EvaluationResponse:
    request = EvaluationRequest(
        expression=expression,
        command=command,
        arguments=arguments,
        options=CalcOptions(),
    )
    return calculate(request, settings)

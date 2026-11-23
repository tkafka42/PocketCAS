"""Berechnen und Befehlsliste."""

from typing import Annotated

from cas.catalog import command_catalog
from fastapi import APIRouter, Depends

from ..auth import require_auth
from ..calculation import calculate
from ..config import Settings, get_settings
from ..schemas import CommandInfo, EvaluationRequest, EvaluationResponse

router = APIRouter(prefix="/api", tags=["calculator"], dependencies=[Depends(require_auth)])


@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate(
    payload: EvaluationRequest,
    settings: Annotated[Settings, Depends(get_settings)],
) -> EvaluationResponse:
    return calculate(payload, settings)


@router.get("/commands", response_model=list[CommandInfo])
def commands() -> tuple[dict, ...]:
    return command_catalog()

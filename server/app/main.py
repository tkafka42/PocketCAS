"""FastAPI-Anwendung von PocketCAS."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import replace

from cas.worker import run_job
from fastapi import FastAPI, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .api import calculator, session, tasks
from .calculation import limits_from
from .config import get_settings
from .errors import AppError

_WARMUP_JOB = {
    "expression": "1+1",
    "command": None,
    "arguments": [],
    "context": [],
    "options": {"mode": "auto", "angle": "rad", "complex_format": "real", "letters_are_constants": False},
}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    # Lädt die Engine einmal vor, damit die erste echte Rechnung nicht ins Zeitlimit läuft.
    await run_in_threadpool(run_job, _WARMUP_JOB, replace(limits_from(settings), timeout_seconds=60))
    yield


app = FastAPI(title="PocketCAS API", version="0.1.0", lifespan=lifespan)
app.include_router(session.router)
app.include_router(calculator.router)
app.include_router(tasks.router)


@app.exception_handler(AppError)
async def handle_app_error(_: Request, error: AppError) -> JSONResponse:
    return JSONResponse(status_code=error.status_code, content=error.body())


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, error: RequestValidationError) -> JSONResponse:
    fields = sorted({".".join(str(part) for part in item["loc"][1:]) for item in error.errors()})
    message = "Ungültige Eingabe" + (f": {', '.join(fields)}." if fields else ".")
    return JSONResponse(status_code=422, content={"code": "VALIDATION_ERROR", "message": message})


@app.get("/api/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}

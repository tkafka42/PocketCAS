"""CRUD für das Heft, mit „letzte Änderung gewinnt“ für den Offline-Sync."""

import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import AwareDatetime
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..auth import require_auth
from ..calculation import recalculate
from ..config import Settings, get_settings
from ..database import get_db
from ..errors import AppError
from ..models import Task
from ..schemas import InputSource, TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"], dependencies=[Depends(require_auth)])

Database = Annotated[Session, Depends(get_db)]
AppSettings = Annotated[Settings, Depends(get_settings)]
_FIELDS = (
    "input_source", "raw_recognition", "expression", "command", "arguments",
    "result_text", "result_latex", "result_decimal", "measurements",
)


def _now() -> datetime:
    return datetime.now(UTC)


def _clamped(value: datetime | None) -> datetime:
    # Eine falsche Handy-Uhr darf spätere Änderungen nicht dauerhaft überstimmen.
    now = _now()
    return now if value is None or value > now else value


def _to_read(task: Task) -> TaskRead:
    data = {field: getattr(task, field) for field in _FIELDS}
    return TaskRead(
        id=task.id,
        has_image=task.image_path is not None,
        created_at=task.created_at,
        updated_at=task.updated_at,
        **data,
    )


def _conflict(task: Task) -> AppError:
    return AppError(
        409,
        "CONFLICT",
        "Diese Aufgabe wurde inzwischen neuer gespeichert.",
        current=_to_read(task).model_dump(mode="json", by_alias=True),
    )


def _not_found() -> AppError:
    return AppError(404, "NOT_FOUND", "Diese Aufgabe gibt es nicht.")


def _remove_image(task: Task, settings: Settings) -> None:
    if not task.image_path:
        return
    root = settings.upload_dir.resolve()
    target = (root / Path(task.image_path).name).resolve()
    if target.parent == root:
        target.unlink(missing_ok=True)
    task.image_path = None


@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: Database,
    search: Annotated[str | None, Query(max_length=200)] = None,
    command: Annotated[str | None, Query(max_length=40)] = None,
    source: InputSource | None = None,
) -> list[TaskRead]:
    query = select(Task).where(Task.deleted_at.is_(None)).order_by(Task.updated_at.desc())
    if search:
        escaped = search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        pattern = f"%{escaped}%"
        query = query.where(or_(
            Task.expression.ilike(pattern, escape="\\"),
            Task.result_text.ilike(pattern, escape="\\"),
        ))
    if command:
        query = query.where(Task.command == command)
    if source:
        query = query.where(Task.input_source == source)
    return [_to_read(task) for task in db.scalars(query)]


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: uuid.UUID, db: Database) -> TaskRead:
    task = db.get(Task, task_id)
    if task is None or task.deleted_at is not None:
        raise _not_found()
    return _to_read(task)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, response: Response, db: Database) -> TaskRead:
    existing = db.get(Task, payload.id)
    if existing is not None:
        if existing.deleted_at is not None:
            raise AppError(409, "TASK_DELETED", "Diese Aufgabe wurde bereits gelöscht.")
        # Wiederholtes Senden aus der Sync-Warteschlange legt nichts doppelt an.
        response.status_code = status.HTTP_200_OK
        return _to_read(existing)
    updated_at = _clamped(payload.updated_at)
    task = Task(
        id=payload.id,
        created_at=min(_clamped(payload.created_at), updated_at),
        updated_at=updated_at,
        **{field: getattr(payload, field) for field in _FIELDS},
    )
    db.add(task)
    db.commit()
    return _to_read(task)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: uuid.UUID, payload: TaskUpdate, db: Database, settings: AppSettings) -> TaskRead:
    task = db.scalar(select(Task).where(Task.id == task_id).with_for_update())
    if task is None:
        raise _not_found()
    updated_at = _clamped(payload.updated_at)
    if task.deleted_at is not None:
        if updated_at <= task.deleted_at:
            raise AppError(409, "TASK_DELETED", "Diese Aufgabe wurde bereits gelöscht.")
        task.deleted_at = None
    elif updated_at < task.updated_at:
        raise _conflict(task)

    values = {field: getattr(payload, field) for field in _FIELDS}
    if payload.recalculate:
        db.rollback()  # Zeilensperre nicht während der Berechnung halten
        result = recalculate(payload.expression, payload.command, payload.arguments, settings)
        values |= {"result_text": result.text, "result_latex": result.latex, "result_decimal": result.decimal}
        task = db.scalar(select(Task).where(Task.id == task_id).with_for_update())
        if task is None:
            raise _not_found()
        if task.deleted_at is not None and updated_at <= task.deleted_at:
            raise AppError(409, "TASK_DELETED", "Diese Aufgabe wurde bereits gelöscht.")
        if task.deleted_at is None and updated_at < task.updated_at:
            raise _conflict(task)
        task.deleted_at = None

    for field, value in values.items():
        setattr(task, field, value)
    task.updated_at = updated_at
    db.commit()
    return _to_read(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: uuid.UUID,
    db: Database,
    settings: AppSettings,
    updated_at: Annotated[AwareDatetime | None, Query(alias="updatedAt")] = None,
) -> Response:
    task = db.scalar(select(Task).where(Task.id == task_id).with_for_update())
    if task is not None and task.deleted_at is None:
        deleted_at = _clamped(updated_at)
        if deleted_at < task.updated_at:
            raise _conflict(task)
        task.deleted_at = deleted_at
        task.updated_at = deleted_at
        _remove_image(task, settings)
        db.commit()
    # Löschen ist idempotent, damit die Sync-Warteschlange gefahrlos wiederholen kann.
    return Response(status_code=status.HTTP_204_NO_CONTENT)

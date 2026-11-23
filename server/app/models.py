"""Datenmodell des Hefts."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import CheckConstraint, DateTime, Index, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

INPUT_SOURCES = ("keypad", "camera", "drawing", "voice", "angle", "gps", "motion")


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "input_source IN ('keypad','camera','drawing','voice','angle','gps','motion')",
            name="ck_tasks_input_source",
        ),
        Index("ix_tasks_active_updated", "updated_at", postgresql_where="deleted_at IS NULL"),
    )

    # Die ID kommt vom Client, damit Aufgaben auch offline angelegt werden können.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    input_source: Mapped[str] = mapped_column(Text)
    image_path: Mapped[str | None] = mapped_column(Text)
    raw_recognition: Mapped[str | None] = mapped_column(Text)
    expression: Mapped[str] = mapped_column(Text)
    command: Mapped[str | None] = mapped_column(Text)
    arguments: Mapped[list[str]] = mapped_column(JSONB, default=list)
    result_text: Mapped[str | None] = mapped_column(Text)
    result_latex: Mapped[str | None] = mapped_column(Text)
    result_decimal: Mapped[str | None] = mapped_column(Text)
    measurements: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    # Grabstein: verhindert, dass Gelöschtes beim Sync zurückkommt.
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

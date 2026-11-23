"""Tabelle für das Heft anlegen.

Revision ID: 0001
Revises:
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("input_source", sa.Text(), nullable=False),
        sa.Column("image_path", sa.Text(), nullable=True),
        sa.Column("raw_recognition", sa.Text(), nullable=True),
        sa.Column("expression", sa.Text(), nullable=False),
        sa.Column("command", sa.Text(), nullable=True),
        sa.Column("arguments", postgresql.JSONB(), nullable=False),
        sa.Column("result_text", sa.Text(), nullable=True),
        sa.Column("result_latex", sa.Text(), nullable=True),
        sa.Column("result_decimal", sa.Text(), nullable=True),
        sa.Column("measurements", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "input_source IN ('keypad','camera','drawing','voice','angle','gps','motion')",
            name="ck_tasks_input_source",
        ),
    )
    op.create_index(
        "ix_tasks_active_updated",
        "tasks",
        ["updated_at"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )


def downgrade() -> None:
    op.drop_index("ix_tasks_active_updated", table_name="tasks")
    op.drop_table("tasks")

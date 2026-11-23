"""Testumgebung: braucht eine eigene, leere Postgres-Datenbank (TEST_DATABASE_URL)."""

import os
import pathlib
import tempfile

import pytest

TEST_PASSWORD = "test-password"
_test_url = os.environ.get("TEST_DATABASE_URL")
if not _test_url:
    raise pytest.UsageError("TEST_DATABASE_URL fehlt. Die Tests leeren diese Datenbank, nutze eine eigene.")

os.environ.update({
    "DATABASE_URL": _test_url,
    "APP_PASSWORD": TEST_PASSWORD,
    "AUTH_SECRET": "test-secret-with-more-than-32-characters",
    "COOKIE_SECURE": "false",
    "UPLOAD_DIR": tempfile.mkdtemp(prefix="pocketcas-uploads-"),
    "CAS_TIMEOUT_SECONDS": "5",
})

from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import text  # noqa: E402

from app.database import get_engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def migrated_database():
    server_root = pathlib.Path(__file__).resolve().parents[1]
    config = Config(str(server_root / "alembic.ini"))
    config.set_main_option("script_location", str(server_root / "migrations"))
    command.upgrade(config, "head")


@pytest.fixture(scope="session")
def anonymous_client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def client(anonymous_client):
    with get_engine().begin() as connection:
        connection.execute(text("TRUNCATE tasks"))
    anonymous_client.cookies.clear()
    response = anonymous_client.post("/api/login", json={"password": TEST_PASSWORD})
    assert response.status_code == 200
    yield anonymous_client
    anonymous_client.cookies.clear()

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 UV_PROJECT_ENVIRONMENT=/opt/venv
RUN pip install --no-cache-dir uv

WORKDIR /srv/server
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY alembic.ini ./
COPY app ./app
COPY cas ./cas
COPY migrations ./migrations

# Der Server läuft ohne Root-Rechte.
RUN useradd --system --uid 10001 pocketcas && mkdir -p uploads && chown pocketcas uploads
USER pocketcas

EXPOSE 8000
CMD ["sh", "-c", "/opt/venv/bin/alembic upgrade head && exec /opt/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers"]

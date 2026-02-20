FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy poetry.lock and pyproject.toml
COPY pyproject.toml .

# Install dependencies
RUN poetry install --without dev --no-interaction

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Task: T027 — Run alembic upgrade head before starting server (FR-018)
# Migrations are idempotent: safe to run on a fresh DB or one already at head.
CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000"]
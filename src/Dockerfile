FROM python:3.11.6 AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install poetry==1.4.2
RUN pip install elastic-apm

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock README.md ./
COPY manage.py ./
COPY src /app/src

RUN poetry install --no-root

FROM python:3.11.6-slim as runtime

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

COPY src/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
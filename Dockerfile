FROM python:3.12-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock README.md ./
COPY . .

RUN poetry install --no-root

FROM python:3.12-slim as runtime

WORKDIR /app

# Instale o netcat também no runtime
RUN apt-get update && apt-get install -y netcat-openbsd

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
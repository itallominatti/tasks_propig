#!/bin/sh
set -e

echo "Aguardando o banco de dados ficar disponível..."
echo "POSTGRES_HOST=$POSTGRES_HOST"
echo "POSTGRES_PORT=$POSTGRES_PORT"

if [ -z "$POSTGRES_PORT" ]; then
  POSTGRES_PORT=5432
fi

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

/app/.venv/bin/python manage.py migrate
exec /app/.venv/bin/python manage.py runserver 0.0.0.0:8000
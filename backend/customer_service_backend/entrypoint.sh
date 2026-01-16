#!/bin/sh

set -e

echo "⏳ Esperando base de datos..."

# Espera a la DB (PostgreSQL)
if [ "$DB_ENGINE" = "postgres" ]; then
  while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 1
  done
fi

echo "✅ Base de datos disponible"

echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📁 Recolectando estáticos (si aplica)..."
python manage.py collectstatic --noinput || true

echo "🚀 Iniciando aplicación..."
exec "$@"

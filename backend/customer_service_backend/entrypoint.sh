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

if [ "$RUN_MIGRATIONS" = "1" ]; then
  echo "📦 Ejecutando migraciones..."
  python manage.py migrate --noinput

  echo "👑 Inicializando roles y superusuario..."
  python manage.py init_roles

  echo "📁 Recolectando estáticos (si aplica)..."
  python manage.py collectstatic --noinput || true
fi

echo "🚀 Iniciando aplicación..."
exec "$@"

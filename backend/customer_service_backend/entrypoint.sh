#!/bin/sh
set -e

echo "🟢 Aplicando migraciones..."
python manage.py migrate --noinput

echo "🟢 Iniciando servidor Django..."
exec "$@"

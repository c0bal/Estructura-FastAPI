#!/bin/sh

# Espera a que la base de datos esté disponible
echo "Esperando a la base de datos en ${DB_HOST}:${DB_PORT}..."
until nc -z ${DB_HOST} ${DB_PORT}; do
  sleep 1
done
echo "✅ Base de datos disponible"

# Ejecuta migraciones
echo "🔁 Ejecutando migraciones con Alembic..."
alembic upgrade head

# Inicia la aplicación con el mismo script que usarías localmente
echo "🚀 Iniciando la aplicación con server.py..."
exec python server.py

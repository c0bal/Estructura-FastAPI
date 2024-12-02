#!/bin/bash

# Exportar variables de entorno desde el archivo .env (si existe)
if [ -f /etc/nginx/.env ]; then
  export $(grep -v '^#' /etc/nginx/.env | xargs)
fi

# Reemplazar variables en la plantilla y generar nginx.conf
envsubst '${API_HOST} ${API_PORT}' < /etc/nginx/nginx.template > /etc/nginx/nginx.conf

# Ejecutar NGINX
nginx -g "daemon off;"

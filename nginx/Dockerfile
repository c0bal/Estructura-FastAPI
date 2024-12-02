# Usamos la imagen base de NGINX
FROM nginx:latest

# Copiamos la plantilla de configuración de NGINX
COPY nginx.template /etc/nginx/nginx.template

# Agregamos un script para reemplazar las variables en la plantilla
COPY start-nginx.sh /usr/local/bin/start-nginx.sh

# Aseguramos permisos de ejecución para el script
RUN chmod +x /usr/local/bin/start-nginx.sh

# Cambiamos el comando de inicio
CMD ["/usr/local/bin/start-nginx.sh"]

# Usamos una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /api

RUN apt-get update && apt-get install -y netcat-openbsd

# Copiar solo los archivos necesarios para instalar las dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

RUN chmod +x initializer.sh

# Comando para iniciar con el script de inicialización
CMD ["./initializer.sh"]
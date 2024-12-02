# Usamos una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /api

# Copiar solo los archivos necesarios para instalar las dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Exponer el puerto que usará la aplicación
EXPOSE 3000

# Comando para iniciar la aplicación con server.py
CMD ["python", "server.py"]

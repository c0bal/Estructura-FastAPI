# syntax=docker/dockerfile:1.6
FROM python:3.11-slim

WORKDIR /api

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd dos2unix && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN dos2unix /api/initializer.sh && chmod 755 /api/initializer.sh

CMD ["/api/initializer.sh"]

# Variables
DOCKER_COMPOSE := sudo docker compose
SYSTEMCTL := sudo systemctl

# Reglas principales
startdocker:
	$(SYSTEMCTL) start docker

# Baja todos los servicios definidos en docker-compose (si fuera necesario)
dockerdown:
	$(DOCKER_COMPOSE) down

# Sube todo con build
dockerup:
	$(DOCKER_COMPOSE) up --build

# Limpieza agresiva (sin tocar Redis)
clear:
	docker container prune -f
	docker volume prune -f
	docker image prune -f

# Limpieza y reinicio completo (excepto redis)
all:
	make startdocker
	make clear
	make dockerdown
	make dockerup

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make startdocker      - Inicia el servicio Docker"
	@echo "  make dockerdown       - Baja todos los servicios con docker-compose"
	@echo "  make dockerup         - Sube los servicios con --build"
	@echo "  make clear             - Limpia contenedores, imágenes y caché"
	@echo "  make all               - Ejecuta un ciclo completo de despliegue"

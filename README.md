# EstructuraFastAPI

Proyecto de backend con FastAPI, Docker, Nginx y PostgreSQL

---

## 🚀 Descripción

Base robusta para aplicaciones backend modernas usando FastAPI, PostgreSQL y Nginx, todo orquestado con Docker. Incluye autenticación JWT, migraciones con Alembic, estructura modular y buenas prácticas para desarrollo y producción.

---

## 🏗️ Arquitectura

- **FastAPI**: Framework principal para la API REST.
- **PostgreSQL**: Base de datos relacional.
- **Alembic**: Migraciones de base de datos.
- **Nginx**: Proxy reverso y servidor estático.
- **Docker**: Contenedores para cada servicio.

```
[Cliente] ⇄ [Nginx] ⇄ [API FastAPI] ⇄ [PostgreSQL]
```

---

## 📁 Estructura de Carpetas y Archivos Principales

### api/

- **main.py**: Punto de entrada de la aplicación FastAPI. Aquí se inicializa la app y se incluyen los routers principales.
- **server.py**: Script de arranque de la aplicación. Suele encargarse de inicializar el servidor y cargar configuraciones.
- **config.py**: Gestiona la configuración global del proyecto, leyendo variables de entorno y definiendo parámetros clave (DB, JWT, etc).
- **log.py**: Configuración y manejo centralizado de logs. Permite registrar eventos, errores y actividad de la aplicación de forma estructurada.
- **requirements.txt**: Lista de dependencias Python necesarias para ejecutar el proyecto. Se instala con `pip install -r requirements.txt`.
- **initializer.sh**: Script de arranque en Docker. Espera la base de datos, ejecuta migraciones Alembic y lanza la app.

#### Carpetas principales:

- **cruds/**: Lógica CRUD (Create, Read, Update, Delete) para cada modelo. Aquí se implementan las funciones que interactúan con la base de datos usando SQLAlchemy. Ejemplo: `user.py` gestiona usuarios con el crud `base.py` que sirve para cualquier modelo simple y con relaciones. Siempre se puede sobreescribir algun método en la propia clase del crud del modelo en caso de querer nuevos metodos.
- **database/**: Maneja la conexión a la base de datos, la sesión y la inicialización de los modelos. Incluye archivos como `db.py` y `session.py`.
- **models/**: Define los modelos de datos con SQLAlchemy, representando las tablas de la base de datos. Ejemplo: `user.py` define el modelo de usuario.
- **routes/**: Define los endpoints de la API. Cada archivo corresponde a un grupo de rutas (usuarios, autenticación, etc). Ejemplo: `auth.py` para login y registro.
- **schemas/**: Define los esquemas Pydantic para validación y serialización de datos en las rutas. Ejemplo: `user.py` para el esquema de usuario.
- **services/**: Servicios auxiliares como autenticación, seguridad, envío de emails, etc. Ejemplo: `auth.py` para lógica de login y generación de tokens.
- **alembic/**: Carpeta de migraciones de base de datos. Permite versionar y actualizar la estructura de la base de datos de forma controlada.

---

## ⚙️ Instalación y Primeros Pasos

1. **Configura variables de entorno:**
   Edita .env descrito mas abajo según tus necesidades (puertos, credenciales, JWT, etc).
2. **Arranca todo con Docker Compose:**
   ```bash
   docker compose up --build
   ```
   O usando Makefile:
   ```bash
   make all
   ```
3. **Accede a la API:**

   - Documentación interactiva: [http://localhost:3000/docs](http://localhost:3000/docs)

   Recomendacion usar Ngnix

   - Nginx: [http://localhost](http://localhost)

---

## 🛠️ Comandos Útiles

- `make startdocker` : Inicia el servicio Docker
- `make dockerdown` : Baja todos los servicios
- `make dockerup` : Sube los servicios con build
- `make clear` : Limpia contenedores, imágenes y volúmenes
- `make all` : Ciclo completo de despliegue

---

## 🗄️ Variables de Entorno (.env)

```env
ENV=dev
SERVER_HOST=0.0.0.0
SERVER_PORT=3000
DB_USER=admin
DB_PASSWORD=password
DB_NAME=db_backend
DB_HOST=db
DB_PORT=5432
JWT_SECRET_KEY=secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

---

## 🧩 Migraciones Alembic

Las migraciones se ejecutan automáticamente al iniciar el contenedor API (`initializer.sh`). Si necesitas crear o aplicar migraciones manualmente:

1. **Entrar al contenedor de la API:**
   ```bash
   docker exec -it api-fastapi-base bash
   ```
2. **Crear una nueva migración:**
   ```bash
   alembic revision --autogenerate -m "mensaje"
   ```
3. **Aplicar migraciones:**
   ```bash
   alembic upgrade head
   ```
4. **Ver el estado de migraciones:**
   ```bash
   alembic history
   alembic current
   ```

> **Recomendación:** Siempre que modifiques los modelos en `models/`, crea y aplica una nueva migración para mantener la base de datos actualizada.

---

## 🔒 Autenticación JWT

- Implementada en `services/auth.py` y `services/security.py`.
- Configura la clave y algoritmo en .env.
- Los endpoints protegidos requieren el header:
  ```http
  Authorization: Bearer <token>
  ```

---

## 📡 Ejemplo de Endpoints

- **Registro de usuario:**
  ```http
  POST /user/register
  {
    "username": "usuario",
    "password": "secreta"
  }
  ```
- **Login y obtención de token:**
  ```http
  POST /auth/login
  {
    "username": "usuario",
    "password": "secreta"
  }
  Respuesta: { "access_token": "...", "token_type": "bearer" }
  ```
- **Endpoint protegido:**
  ```http
  GET /user
  Header: Authorization: Bearer <token>
  ```

---

## 📝 Recomendaciones y Buenas Prácticas

- Usa Docker para desarrollo y producción.
- Mantén tus claves y contraseñas fuera del código.
- Revisa y adapta los modelos y rutas según tu caso de uso.
- Actualiza las migraciones cada vez que cambies los modelos.

- Consulta la documentación interactiva en `/docs`.

- Si agregas nuevas rutas, solo inclúyelas en `routes/__init__.py` y se cargarán automáticamente en el despliegue.

---

## 📚 Recursos

- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://docs.docker.com/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Nginx](https://nginx.org/)
- [PostgreSQL](https://www.postgresql.org/)

---

## 👨‍💻 Autor

- Cristobal Merino L.

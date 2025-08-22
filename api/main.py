from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from log import get_logger
import routes

log = get_logger(__name__)

app = FastAPI(title="EasyCancha API", version="1.0.0")

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    log.info("Accessing API root endpoint.")
    return {"message": "Welcome to FastApi Base API!"}

for router_name in routes.__all__:
    router = getattr(routes, router_name)
    app.include_router(router)
    log.info(f"Router {router_name} registrado correctamente.")

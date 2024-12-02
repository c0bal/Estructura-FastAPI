from fastapi import FastAPI
from log import get_logger

log = get_logger(__name__)

app = FastAPI(title="API Server", version="1.0.0")

# Root endpoint
@app.get("/")
def root():
    log.info("Accessing API root endpoint.")
    return {"message": "Welcome to your API!"}

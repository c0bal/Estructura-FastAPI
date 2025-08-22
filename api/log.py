import logging
import sys
import os
from typing import Optional

LOGGING_FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

ENV_LOG_LEVELS = {
    "dev": "DEBUG",
    "prod": "INFO"
}

def get_logger(name: Optional[str] = None, level: Optional[str] = None) -> logging.Logger:
    log = logging.getLogger(name)
    
    # Evita múltiples handlers si ya fue configurado
    if not log.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(LOGGING_FORMATTER)
        handler.setFormatter(formatter)
        log.addHandler(handler)

    # Si no se pasa el nivel explícitamente, lo tomamos según ENV
    if not level:
        env = os.getenv("ENV", "dev").lower()
        level = ENV_LOG_LEVELS.get(env, "DEBUG")

    log.setLevel(level)

    return log

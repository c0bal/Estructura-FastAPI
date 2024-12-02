import logging
import sys
from typing import Optional

LOGGING_FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

DebugLevels = ["DEBUG", "INFO", "WARNING", "ERROR"]
DebugLevelType = str

def get_logger(name: Optional[str] = None, level: DebugLevelType = "DEBUG") -> logging.Logger:
    
    log = logging.getLogger(name=name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(LOGGING_FORMATTER)
    handler.setFormatter(formatter)
    log.addHandler(handler)

    if not level or level not in DebugLevels:
        log.warning("Invalid logging level %s. Setting logging level to DEBUG.", level)
        level = "DEBUG"

    log.setLevel(level=level)
    return log

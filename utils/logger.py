import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_json(level: str, message: str, extra: dict = None):
    log_data = {"level": level, "message": message}
    if extra:
        log_data["extra"] = extra
    print(json.dumps(log_data))
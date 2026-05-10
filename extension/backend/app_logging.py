import os
import sys
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

def setup_logging(name="promptify_backend"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        # Use /tmp for writable storage (works in Appwrite and locally)
        log_dir = "/tmp/logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "app.log")
        file_handler = ConcurrentRotatingFileHandler(log_file, "a", 10 * 1024 * 1024, 5)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass  # File logging unavailable, console only

    return logger

logger = setup_logging()

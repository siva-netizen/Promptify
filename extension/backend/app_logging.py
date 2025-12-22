import os
import sys
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

def setup_logging(name="promptify_backend"):
    """
    Configures and returns a logger with concurrent file handling and console output.
    """
    # Ensure log directory exists
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid adding handlers multiple times if function is called repeatedly
    if logger.handlers:
        return logger

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 1. Console Handler (Stream)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. File Handler (Concurrent & Rotating)
    # 10MB limit, 5 backups
    file_handler = ConcurrentRotatingFileHandler(log_file, "a", 10 * 1024 * 1024, 5) 
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Create a default logger instance for easy import
logger = setup_logging()

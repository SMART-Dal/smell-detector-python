import logging
import os
import datetime
from logging.handlers import RotatingFileHandler

# Environment setup
ENVIRONMENT = os.getenv('ENVIRONMENT', 'prod').lower()
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG' if ENVIRONMENT == 'development' else 'INFO').upper()

# Default log directory setup
DEFAULT_LOG_DIRECTORY = "logs" if ENVIRONMENT == 'development' else '/var/log/smell_detector_python'
LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
NUM_LOG_FILES_BACKUP = 5

# Log format
LOG_FORMAT = '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def ensure_log_directory_exists(log_directory):
    """Ensure that the log directory exists."""
    try:
        os.makedirs(log_directory, exist_ok=True)
    except Exception as e:
        logging.error(f"Error creating log directory: {e}")
        return None
    return log_directory


def setup_logging(log_directory=None):
    """Set up logging with rotating file handler."""
    if not log_directory:
        log_directory = DEFAULT_LOG_DIRECTORY  # Fallback to the default if not provided

    log_directory = ensure_log_directory_exists(log_directory)
    if not log_directory:
        print("Logging will be directed to the console due to an issue with the log directory.")
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_filename = os.path.join(log_directory, f"log_{timestamp}.log")

    # Configure root logger
    logger = logging.getLogger('')
    logger.setLevel(LOG_LEVEL)

    # Rotating file handler
    rotate_handler = RotatingFileHandler(log_filename, maxBytes=LOG_FILE_MAX_SIZE, backupCount=NUM_LOG_FILES_BACKUP)
    rotate_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(rotate_handler)

    # Console handler for development
    if ENVIRONMENT == 'development':
        print("Logging will be directed to the console")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
        logger.addHandler(console_handler)


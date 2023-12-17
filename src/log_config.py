import logging
import os
import datetime


def setup_logging(log_directory="logs"):
    # Create a directory for logs if it does not exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Generate a log file name with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_filename = os.path.join(log_directory, f"log_{timestamp}.log")

    # Set up logging configuration
    logging.basicConfig(
        filename=log_filename,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


# Call this at the start of your script
setup_logging()

# Example usage
logging.debug("This is a debug message")
logging.info("This is an informational message")

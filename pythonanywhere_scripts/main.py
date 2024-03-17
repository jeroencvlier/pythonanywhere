import os
import logging

from pythonanywhere_scripts.local_rsync import local_rsync
from pythonanywhere_scripts.s3_sync import aws_sync


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def is_running_on_pythonanywhere():
    """Check if the script is running on PythonAnywhere."""
    return "PYTHONANYWHERE_DOMAIN" in os.environ


def main():
    """Run the appropriate sync function based on the environment."""
    if is_running_on_pythonanywhere():
        logging.info("Running on PythonAnywhere.")
        aws_sync()
    else:
        logging.info("Running locally or on another environment.")
        local_rsync()


if __name__ == "__main__":
    main()

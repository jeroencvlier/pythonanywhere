import os
import logging
import local_rsync, s3_sync

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def is_running_on_pythonanywhere():
    """Check if the script is running on PythonAnywhere."""
    return "PYTHONANYWHERE_DOMAIN" in os.environ


def main():
    """Run the appropriate sync function based on the environment."""
    if is_running_on_pythonanywhere():
        logging.info("Running on PythonAnywhere.")
        s3_sync()
    else:
        logging.info("Running locally or on another environment.")
        local_rsync()


if __name__ == "__main__":
    main()

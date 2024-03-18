import os
import sys
import logging
import argparse

from pythonanywhere_scripts.local_rsync import local_rsync
from pythonanywhere_scripts.s3_sync import aws_sync
from pythonanywhere_scripts import telegram_bot

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def is_running_on_pythonanywhere():
    """Check if the script is running on PythonAnywhere."""
    return "PYTHONANYWHERE_DOMAIN" in os.environ

def main():
    """Run the appropriate sync function based on the environment."""
    parser = argparse.ArgumentParser(description="Sync data and optionally test Telegram notifications.")
    parser.add_argument("--telegram-test", action="store_true", help="Run a test for Telegram notifications.")
    args = parser.parse_args()

    if args.telegram_test:
        logging.info("Running Telegram test.")
        telegram_bot.send_mess("Test message from sync script.")
    elif is_running_on_pythonanywhere():
        logging.info("Running on PythonAnywhere.")
        aws_sync()
    else:
        logging.info("Running locally or on another environment.")
        local_rsync()

    sys.exit(0)

if __name__ == "__main__":
    main()

import subprocess
import sys
import datetime as dt
import logging

# import telegram_bot
import time

from pythonanywhere_scripts import telegram_bot
from pythonanywhere_scripts.utils import fetch_weeks_cloud
from pythonanywhere_scripts.utils import storage_check

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


# check if is is weekday or weekend
def is_weekday(todays_date=dt.datetime.today()):
    return todays_date.weekday() < 5


def count_files_uploaded(output):
    return output.count("upload:")


def aws_sync():
    start_time = time.time()
    week_list = fetch_weeks_cloud(pull_latest_week_only=is_weekday())
    total_files_uploaded = 0
    for week in week_list:
        message = f"Pulling Option Data for {week}!"
        logging.info(message)
        aws_command = [
            "/home/jeroencvlier/.virtualenvs/awssync/bin/aws",
            "s3",
            "sync",
            f"/home/jeroencvlier/option_chain_data/{week}/",
            "s3://option-chain-data-backup/option_chain_data",
            # "--size-only",
            # "--exclude",
            # '"*"',
            # "--include",
            # "*.json.gz",
            "--profile",
            "default",
        ]

        try:
            result = subprocess.run(
                aws_command,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Parsing rsync output for the number of files transferred
            week_file_count = 0

            for line in result.stdout.split("\n"):
                if line.strip().endswith(".json.gz"):
                    week_file_count += 1
                    total_files_uploaded += 1

        except subprocess.CalledProcessError as e:
            logging.error(f"Rsync failed for {week}: {e}")
            message += f"\n\nError {week}: " + str(e)[:200] + "\n\n"

        # send tim ein HH:mm:ss format and remove milliseconds
        message += f"\n\nTotal time taken for : {str(dt.timedelta(seconds=(time.time() - start_time)))[:-7]} HH:mm:ss"
        message += f"\nTotal files uploaded: {total_files_uploaded}"
        message += storage_check()
        try:
            telegram_bot.send_mess(message)
        except Exception as error:
            logging.error("Failed to send message to telegram.")
            logging.error(error)

    return message


if __name__ == "__main__":
    # run the script
    message = aws_sync()
    # check storage
    message += storage_check()
    # send telegram message
    telegram_bot.send_mess(message)

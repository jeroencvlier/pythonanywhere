import subprocess
import sys
import datetime as dt

# import telegram_bot

from pythonanywhere_scripts import telegram_bot
from pythonanywhere_scripts.utils import fetch_weeks_cloud
from pythonanywhere_scripts.utils import storage_check
# def count_files_uploaded(output):
#     count = 0
#     lines = output.split("\n")
#     for line in lines:
#         if "upload:" in line:
#             count += 1
#     return count


# check if is is weekday or weekend
def is_weekday(todays_date):
    return todays_date.weekday() < 5


def count_files_uploaded(output):
    return output.count("upload:")


def aws_sync():
    todays_date = dt.datetime.today()
    week_list = fetch_weeks_cloud(last_week=is_weekday(todays_date))
    for week in week_list:
        total_files_uploaded = 0
        message = f"Pulling Option Data for {week}!"
        print(message)
        aws_command = [
            "/home/jeroencvlier/.virtualenvs/awssync/bin/aws",
            "s3",
            "sync",
            f"/home/jeroencvlier/option_chain_data/{week}/",
            "s3://option-chain-data-backup/option_chain_data",
            "--size-only",
            "--exclude",
            '"*"',
            "--include",
            "*.json.gz",
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
            total_files_uploaded += count_files_uploaded(result.stdout)

        except subprocess.CalledProcessError as error:
            print("Error:")
            print(error.stderr)
            message += f"\nError: " + str(error.stderr)[:200]

        message = f"Total files uploaded: {total_files_uploaded}"

    return message








if __name__ == "__main__":
    # run the script
    message = aws_sync()
    # check storage
    message += storage_check()
    # send telegram message
    telegram_bot.send_mess(message)
    sys.exit(0)
